/* eslint-disable @typescript-eslint/no-explicit-any */
export {};

declare global {
  interface Window {
    pywebview: {
      api: {
        [key: string]: (...args: any[]) => Promise<any>;
      };
    };
  }
}