/**
 * Icon Name Mappings
 * Semantic icon names mapped to lucide-react component names.
 * Provides a single source of truth for icon usage across the app.
 * 
 * Usage:
 * ```tsx
 * import { ICON_NAMES } from "@/constants/icons";
 * <Icon name={ICON_NAMES.SUCCESS} size="base" />
 * ```
 */

export const ICON_NAMES = {
  // Status & Feedback
  SUCCESS: "CheckCircle2",
  ERROR: "AlertCircle",
  WARNING: "AlertTriangle",
  INFO: "Info",
  CLOSE: "X",

  // Navigation
  MENU: "Menu",
  CHEVRON_DOWN: "ChevronDown",
  CHEVRON_UP: "ChevronUp",
  CHEVRON_LEFT: "ChevronLeft",
  CHEVRON_RIGHT: "ChevronRight",
  HOME: "Home",
  ARROW_RIGHT: "ArrowRight",
  ARROW_LEFT: "ArrowLeft",

  // Auth & User
  USER: "User",
  LOGOUT: "LogOut",
  LOGIN: "LogIn",
  LOCK: "Lock",
  UNLOCK: "Unlock",
  SETTINGS: "Settings",
  PROFILE: "UserCircle",

  // Media
  VOLUME: "Volume2",
  VOLUME_MUTE: "VolumeX",
  PLAY: "Play",
  PAUSE: "Pause",
  MICROPHONE: "Mic",
  MICROPHONE_OFF: "MicOff",
  IMAGE: "Image",
  MUSIC: "Music",
  VIDEO: "Video",

  // Learning & Difficulty
  STAR: "Star",
  FLAME: "Flame",
  ZAPS: "Zap",
  BOOK: "BookOpen",
  LIGHTBULB: "Lightbulb",
  TARGET: "Target",
  TRENDING_UP: "TrendingUp",

  // UI Controls
  SEARCH: "Search",
  FILTER: "Filter",
  DOWNLOAD: "Download",
  UPLOAD: "Upload",
  SHARE: "Share2",
  COPY: "Copy",
  EDIT: "Edit",
  TRASH: "Trash2",
  EYE: "Eye",
  EYE_OFF: "EyeOff",
  CLOCK: "Clock",
  CALENDAR: "Calendar",

  // Misc
  HELP: "HelpCircle",
  LOADER: "Loader2",
  CHECK: "Check",
  X: "X",
} as const;

export type IconName = (typeof ICON_NAMES)[keyof typeof ICON_NAMES];
