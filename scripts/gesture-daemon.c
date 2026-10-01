#define _DEFAULT_SOURCE
#define _POSIX_C_SOURCE 200809L

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <time.h>
#include <math.h>
#include <signal.h>
#include <errno.h>
#include <fcntl.h>
#include <X11/Xlib.h>
#include <X11/keysym.h>
#include <X11/extensions/XInput2.h>
#include <X11/extensions/XTest.h>

#define DEFAULT_SWIPE_THRESHOLD 20.0
#define DEFAULT_PINCH_SCALE_UP   1.22
#define DEFAULT_PINCH_SCALE_DOWN 0.78
#define DEFAULT_DEBOUNCE_MS     180

static Display *dpy = NULL;
static int verbose_mode = 0;
static char pid_file_path[512] = {0};

static double swipe_threshold = DEFAULT_SWIPE_THRESHOLD;
static double pinch_scale_up = DEFAULT_PINCH_SCALE_UP;
static double pinch_scale_down = DEFAULT_PINCH_SCALE_DOWN;
static int debounce_ms = DEFAULT_DEBOUNCE_MS;

static long long current_time_ms(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (long long)ts.tv_sec * 1000LL + (ts.tv_nsec / 1000000LL);
}

static void remove_pid_file(void) {
    if (pid_file_path[0] != '\0') {
        unlink(pid_file_path);
    }
}

static void cleanup_and_exit(int sig) {
    (void)sig;
    remove_pid_file();
    if (dpy) {
        XCloseDisplay(dpy);
        dpy = NULL;
    }
    _exit(0);
}

static int x_error_occurred = 0;
static int custom_x_error_handler(Display *d, XErrorEvent *e) {
    (void)d;
    x_error_occurred = e->error_code;
    if (verbose_mode) {
        char buf[256];
        XGetErrorText(d, e->error_code, buf, sizeof(buf));
        fprintf(stderr, "[gesture-daemon] X Error: %s (code %d, request %d, minor %d)\n",
                buf, e->error_code, e->request_code, e->minor_code);
    }
    return 0;
}

static void get_pid_path(void) {
    const char *runtime_dir = getenv("XDG_RUNTIME_DIR");
    if (runtime_dir && runtime_dir[0] != '\0') {
        snprintf(pid_file_path, sizeof(pid_file_path), "%s/qtile-gesture-daemon.pid", runtime_dir);
    } else {
        const char *user = getenv("USER");
        if (!user) user = "user";
        snprintf(pid_file_path, sizeof(pid_file_path), "/tmp/qtile-gesture-%s.pid", user);
    }
}

static pid_t read_running_pid(void) {
    get_pid_path();
    FILE *f = fopen(pid_file_path, "r");
    if (!f) return 0;
    pid_t pid = 0;
    if (fscanf(f, "%d", &pid) == 1 && pid > 1) {
        fclose(f);
        if (kill(pid, 0) == 0) {
            return pid;
        }
    } else {
        fclose(f);
    }
    unlink(pid_file_path);
    return 0;
}

static void write_pid_file(pid_t pid) {
    get_pid_path();
    FILE *f = fopen(pid_file_path, "w");
    if (f) {
        fprintf(f, "%d\n", pid);
        fclose(f);
    }
}

/*
 * Ultra-fast direct keypress simulation via XTest.
 * Takes < 0.1ms (no shell forks or python interpreter overhead).
 */
static void send_key_combo(Display *d, KeySym mod1, KeySym mod2, KeySym mod3, KeySym key) {
    if (!d) return;
    KeyCode kc_m1 = mod1 ? XKeysymToKeycode(d, mod1) : 0;
    KeyCode kc_m2 = mod2 ? XKeysymToKeycode(d, mod2) : 0;
    KeyCode kc_m3 = mod3 ? XKeysymToKeycode(d, mod3) : 0;
    KeyCode kc_k  = key  ? XKeysymToKeycode(d, key)  : 0;

    if (verbose_mode) {
        printf("[gesture-daemon] Fast XTest key combo: mod1=%lu mod2=%lu mod3=%lu key=%lu\n",
               (unsigned long)mod1, (unsigned long)mod2, (unsigned long)mod3, (unsigned long)key);
        fflush(stdout);
    }

    // Press modifiers & key
    if (kc_m1) XTestFakeKeyEvent(d, kc_m1, True, CurrentTime);
    if (kc_m2) XTestFakeKeyEvent(d, kc_m2, True, CurrentTime);
    if (kc_m3) XTestFakeKeyEvent(d, kc_m3, True, CurrentTime);
    if (kc_k)  XTestFakeKeyEvent(d, kc_k,  True, CurrentTime);
    XSync(d, False);

    usleep(15000); // 15ms hold time for reliable X11 key grab detection

    // Release key & modifiers
    if (kc_k)  XTestFakeKeyEvent(d, kc_k,  False, CurrentTime);
    if (kc_m3) XTestFakeKeyEvent(d, kc_m3, False, CurrentTime);
    if (kc_m2) XTestFakeKeyEvent(d, kc_m2, False, CurrentTime);
    if (kc_m1) XTestFakeKeyEvent(d, kc_m1, False, CurrentTime);

    XSync(d, False);
}

static void handle_swipe(int fingers, double dx, double dy) {
    if (fingers == 3) {
        if (fabs(dx) > fabs(dy)) {
            if (dx < 0) {
                // Swipe left (natural scrolling) -> next workspace (super+alt+Right)
                send_key_combo(dpy, XK_Super_L, XK_Alt_L, 0, XK_Right);
            } else {
                // Swipe right (natural scrolling) -> prev workspace (super+alt+Left)
                send_key_combo(dpy, XK_Super_L, XK_Alt_L, 0, XK_Left);
            }
        } else {
            if (dy < 0) {
                // Swipe up -> next layout (super+alt+Up)
                send_key_combo(dpy, XK_Super_L, XK_Alt_L, 0, XK_Up);
            } else {
                // Swipe down -> prev layout (super+alt+Down)
                send_key_combo(dpy, XK_Super_L, XK_Alt_L, 0, XK_Down);
            }
        }
    } else if (fingers == 4) {
        if (fabs(dx) > fabs(dy)) {
            if (dx < 0) {
                // 4-finger left (natural scrolling) -> window to next group (super+alt+shift+Right)
                send_key_combo(dpy, XK_Super_L, XK_Alt_L, XK_Shift_L, XK_Right);
            } else {
                // 4-finger right (natural scrolling) -> window to prev group (super+alt+shift+Left)
                send_key_combo(dpy, XK_Super_L, XK_Alt_L, XK_Shift_L, XK_Left);
            }
        } else {
            if (dy < 0) {
                // 4-finger up -> open application launcher (super+alt+Return)
                send_key_combo(dpy, XK_Super_L, XK_Alt_L, 0, XK_Return);
            } else {
                // 4-finger down -> open terminal (super+alt+shift+Return)
                send_key_combo(dpy, XK_Super_L, XK_Alt_L, XK_Shift_L, XK_Return);
            }
        }
    }
}

static void print_usage(const char *progname) {
    printf("Qtile-Con Ultra-Fast Native X11 Gesture Daemon (libinput driven)\n");
    printf("Usage: %s [OPTIONS]\n\n", progname);
    printf("Options:\n");
    printf("  -d, --daemon            Run in background as daemon (default)\n");
    printf("  -f, --foreground        Run in foreground (useful for debugging)\n");
    printf("  -v, --verbose           Enable verbose event logging\n");
    printf("  -t, --threshold <px>    Swipe distance threshold (default: 20.0)\n");
    printf("  -b, --debounce <ms>     Debounce cooldown in ms (default: 180)\n");
    printf("  -k, --kill              Stop any currently running gesture daemon\n");
    printf("  -r, --restart           Restart the gesture daemon\n");
    printf("  -s, --status            Check daemon status\n");
    printf("  -h, --help              Show this help message\n");
}

int main(int argc, char **argv) {
    int foreground_mode = 0;
    int kill_mode = 0;
    int restart_mode = 0;
    int status_mode = 0;

    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-f") == 0 || strcmp(argv[i], "--foreground") == 0) {
            foreground_mode = 1;
        } else if (strcmp(argv[i], "-v") == 0 || strcmp(argv[i], "--verbose") == 0) {
            verbose_mode = 1;
        } else if (strcmp(argv[i], "-d") == 0 || strcmp(argv[i], "--daemon") == 0) {
            foreground_mode = 0;
        } else if (strcmp(argv[i], "-t") == 0 || strcmp(argv[i], "--threshold") == 0) {
            if (i + 1 < argc) {
                swipe_threshold = atof(argv[++i]);
                if (swipe_threshold < 5.0) swipe_threshold = 5.0;
            }
        } else if (strcmp(argv[i], "-b") == 0 || strcmp(argv[i], "--debounce") == 0) {
            if (i + 1 < argc) {
                debounce_ms = atoi(argv[++i]);
                if (debounce_ms < 50) debounce_ms = 50;
            }
        } else if (strcmp(argv[i], "-k") == 0 || strcmp(argv[i], "--kill") == 0 || strcmp(argv[i], "--stop") == 0) {
            kill_mode = 1;
        } else if (strcmp(argv[i], "-r") == 0 || strcmp(argv[i], "--restart") == 0) {
            restart_mode = 1;
        } else if (strcmp(argv[i], "-s") == 0 || strcmp(argv[i], "--status") == 0) {
            status_mode = 1;
        } else if (strcmp(argv[i], "-h") == 0 || strcmp(argv[i], "--help") == 0) {
            print_usage(argv[0]);
            return 0;
        }
    }

    pid_t existing_pid = read_running_pid();

    if (status_mode) {
        if (existing_pid > 0) {
            printf("[OK] gesture-daemon is running (PID: %d).\n", existing_pid);
            return 0;
        } else {
            printf("[INFO] gesture-daemon is not running.\n");
            return 1;
        }
    }

    if (kill_mode || restart_mode) {
        if (existing_pid > 0) {
            kill(existing_pid, SIGTERM);
            usleep(150000);
            if (kill(existing_pid, 0) == 0) {
                kill(existing_pid, SIGKILL);
            }
            remove_pid_file();
            printf("[OK] Stopped existing gesture-daemon (PID: %d).\n", existing_pid);
        } else {
            if (kill_mode) {
                printf("[INFO] No existing gesture-daemon was running.\n");
                return 0;
            }
        }
        if (kill_mode) return 0;
    } else if (existing_pid > 0) {
        if (verbose_mode) {
            printf("[INFO] gesture-daemon already running (PID: %d).\n", existing_pid);
        }
        return 0;
    }

    // If not foreground, daemonize before opening X display
    if (!foreground_mode) {
        if (daemon(1, 0) != 0) {
            perror("daemon");
            return 1;
        }
    }

    // Write our PID
    write_pid_file(getpid());

    signal(SIGINT, cleanup_and_exit);
    signal(SIGTERM, cleanup_and_exit);
    signal(SIGHUP, SIG_IGN);
    signal(SIGPIPE, SIG_IGN);
    signal(SIGCHLD, SIG_IGN);

    dpy = XOpenDisplay(NULL);
    if (!dpy) {
        fprintf(stderr, "qtile-gesture-daemon: Cannot open X display %s\n", XDisplayName(NULL));
        remove_pid_file();
        return 1;
    }

    XSetErrorHandler(custom_x_error_handler);

    int xi_opcode, event, error;
    if (!XQueryExtension(dpy, "XInputExtension", &xi_opcode, &event, &error)) {
        fprintf(stderr, "qtile-gesture-daemon: XInputExtension not available\n");
        cleanup_and_exit(1);
    }

    int major = 2, minor = 4;
    if (XIQueryVersion(dpy, &major, &minor) != Success || major < 2 || (major == 2 && minor < 4)) {
        fprintf(stderr, "qtile-gesture-daemon: XInput 2.4+ required (found %d.%d)\n", major, minor);
        cleanup_and_exit(1);
    }

    Window root = DefaultRootWindow(dpy);

    // Register event mask for master pointer devices
    XIEventMask mask[2];
    unsigned char mask_bytes1[XIMaskLen(XI_LASTEVENT)] = {0};
    unsigned char mask_bytes2[XIMaskLen(XI_LASTEVENT)] = {0};

    mask[0].deviceid = XIAllMasterDevices;
    mask[0].mask_len = sizeof(mask_bytes1);
    mask[0].mask = mask_bytes1;

    XISetMask(mask[0].mask, XI_GestureSwipeBegin);
    XISetMask(mask[0].mask, XI_GestureSwipeUpdate);
    XISetMask(mask[0].mask, XI_GestureSwipeEnd);
    XISetMask(mask[0].mask, XI_GesturePinchBegin);
    XISetMask(mask[0].mask, XI_GesturePinchUpdate);
    XISetMask(mask[0].mask, XI_GesturePinchEnd);

    mask[1].deviceid = XIAllDevices;
    mask[1].mask_len = sizeof(mask_bytes2);
    mask[1].mask = mask_bytes2;

    XISetMask(mask[1].mask, XI_GestureSwipeBegin);
    XISetMask(mask[1].mask, XI_GestureSwipeUpdate);
    XISetMask(mask[1].mask, XI_GestureSwipeEnd);
    XISetMask(mask[1].mask, XI_GesturePinchBegin);
    XISetMask(mask[1].mask, XI_GesturePinchUpdate);
    XISetMask(mask[1].mask, XI_GesturePinchEnd);

    x_error_occurred = 0;
    XISelectEvents(dpy, root, mask, 2);
    XSync(dpy, False);

    if (x_error_occurred != 0) {
        if (x_error_occurred == BadAccess) {
            fprintf(stderr, "qtile-gesture-daemon: Another gesture client or daemon already has an exclusive grab on gesture events.\n");
        } else {
            fprintf(stderr, "qtile-gesture-daemon: Failed to select XI2 gesture events (X error %d)\n", x_error_occurred);
        }
        cleanup_and_exit(1);
    }

    if (verbose_mode) {
        printf("[gesture-daemon] Successfully initialized on display %s. Threshold=%.1f, Debounce=%dms\n",
               XDisplayName(NULL), swipe_threshold, debounce_ms);
        fflush(stdout);
    }

    double swipe_dx = 0.0, swipe_dy = 0.0;
    int swipe_triggered = 0;
    int swipe_fingers = 0;
    long long last_action_time = 0;

    int pinch_triggered = 0;

    XEvent ev;
    while (1) {
        XNextEvent(dpy, &ev);
        if (ev.xcookie.type == GenericEvent && ev.xcookie.extension == xi_opcode) {
            if (XGetEventData(dpy, &ev.xcookie)) {
                int evtype = ev.xcookie.evtype;
                long long now = current_time_ms();

                if (evtype == XI_GestureSwipeBegin) {
                    XIGestureSwipeEvent *g = (XIGestureSwipeEvent *)ev.xcookie.data;
                    swipe_fingers = g->detail;
                    swipe_dx = 0.0;
                    swipe_dy = 0.0;
                    swipe_triggered = 0;
                } else if (evtype == XI_GestureSwipeUpdate) {
                    XIGestureSwipeEvent *g = (XIGestureSwipeEvent *)ev.xcookie.data;
                    swipe_dx += g->delta_x;
                    swipe_dy += g->delta_y;

                    if (!swipe_triggered && (now - last_action_time >= debounce_ms)) {
                        if (fabs(swipe_dx) >= swipe_threshold || fabs(swipe_dy) >= swipe_threshold) {
                            if (verbose_mode) {
                                printf("[gesture-daemon] Swipe detected: %d fingers, dx=%.1f, dy=%.1f (threshold=%.1f)\n",
                                       swipe_fingers, swipe_dx, swipe_dy, swipe_threshold);
                            }
                            handle_swipe(swipe_fingers, swipe_dx, swipe_dy);
                            swipe_triggered = 1;
                            last_action_time = now;
                        }
                    }
                } else if (evtype == XI_GestureSwipeEnd) {
                    swipe_dx = 0.0;
                    swipe_dy = 0.0;
                    swipe_triggered = 0;
                    swipe_fingers = 0;
                } else if (evtype == XI_GesturePinchBegin) {
                    pinch_triggered = 0;
                } else if (evtype == XI_GesturePinchUpdate) {
                    XIGesturePinchEvent *g = (XIGesturePinchEvent *)ev.xcookie.data;
                    if (!pinch_triggered && (now - last_action_time >= debounce_ms)) {
                        if (g->scale >= pinch_scale_up) {
                            if (verbose_mode) {
                                printf("[gesture-daemon] Pinch out detected (scale=%.2f)\n", g->scale);
                            }
                            send_key_combo(dpy, XK_Super_L, XK_Alt_L, 0, XK_f);
                            pinch_triggered = 1;
                            last_action_time = now;
                        } else if (g->scale <= pinch_scale_down) {
                            if (verbose_mode) {
                                printf("[gesture-daemon] Pinch in detected (scale=%.2f)\n", g->scale);
                            }
                            send_key_combo(dpy, XK_Super_L, XK_Alt_L, 0, XK_space);
                            pinch_triggered = 1;
                            last_action_time = now;
                        }
                    }
                } else if (evtype == XI_GesturePinchEnd) {
                    pinch_triggered = 0;
                }

                XFreeEventData(dpy, &ev.xcookie);
            }
        }
    }

    cleanup_and_exit(0);
    return 0;
}
