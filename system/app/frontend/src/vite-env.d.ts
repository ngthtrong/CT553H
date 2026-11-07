/// <reference types="vite/client" />

interface ImportMetaEnv {
  /** Optional absolute API origin; empty means same origin (proxy or nginx). */
  readonly VITE_API_BASE?: string;
}
