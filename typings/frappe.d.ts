/** Minimal type declarations for global Frappe APIs used in this project. */
declare const __: (text: string) => string;

declare namespace frappe {
  namespace ui {
    namespace form {
      function on(doctype: string, handlers: Record<string, unknown>): void;
    }
  }
  function call(options: Record<string, unknown>): void;
  function set_route(...args: unknown[]): void;
  function new_doc(doctype: string, opts?: Record<string, unknown>): void;
  const db: unknown;
}
