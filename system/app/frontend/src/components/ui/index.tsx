/**
 * Shared interface primitives (implementation plan WP1.6). Every control reaches 44 px, carries a visible label or an
 * accessible name, and never signals state by colour alone (icon + text). Styles: src/styles/ui.css.
 */
import {
  type ButtonHTMLAttributes,
  type KeyboardEvent,
  type ReactNode,
  type SelectHTMLAttributes,
  useEffect,
  useId,
  useRef,
  useState,
} from 'react';
import {
  AlertTriangle,
  ArrowDown,
  ArrowUp,
  ArrowUpDown,
  Ban,
  CheckCircle2,
  ChevronLeft,
  ChevronRight,
  CircleDashed,
  Clock,
  Info,
  Loader2,
  type LucideIcon,
  OctagonX,
  X,
  XCircle,
} from 'lucide-react';

const cx = (...parts: (string | false | null | undefined)[]) => parts.filter(Boolean).join(' ');

// --- Button / IconButton ---------------------------------------------------------------------------------------------

type Variant = 'primary' | 'secondary' | 'ghost' | 'danger';

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
  icon?: LucideIcon;
  busy?: boolean;
}

export function Button({ variant = 'secondary', icon: Icon, busy = false, className, children, disabled, ...rest }: ButtonProps) {
  return (
    <button
      type="button"
      {...rest}
      className={cx('ui-button', `ui-button--${variant}`, className)}
      disabled={disabled || busy}
      aria-busy={busy || undefined}
    >
      {busy ? <Loader2 className="ui-spin" size={18} aria-hidden="true" /> : Icon && <Icon size={18} aria-hidden="true" />}
      <span>{children}</span>
    </button>
  );
}

export interface IconButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  icon: LucideIcon;
  /** Required: an icon alone is not a name (WCAG 4.1.2). */
  label: string;
}

export function IconButton({ icon: Icon, label, className, ...rest }: IconButtonProps) {
  return (
    <button type="button" {...rest} className={cx('ui-icon-button', className)} aria-label={label} title={label}>
      <Icon size={20} aria-hidden="true" />
    </button>
  );
}

// --- Field / Select --------------------------------------------------------------------------------------------------

export interface FieldProps {
  label: string;
  hint?: ReactNode;
  error?: string | null;
  required?: boolean;
  /** Receives the ids to wire the control: id, aria-describedby, aria-invalid. */
  children: (ids: { id: string; describedBy: string | undefined; invalid: boolean }) => ReactNode;
}

export function Field({ label, hint, error, required, children }: FieldProps) {
  const id = useId();
  const hintId = hint ? `${id}-hint` : undefined;
  const errId = error ? `${id}-err` : undefined;
  const describedBy = [errId, hintId].filter(Boolean).join(' ') || undefined;
  return (
    <div className={cx('ui-field', error && 'ui-field--invalid')}>
      <label htmlFor={id} className="ui-field__label">
        {label}
        {required && <span className="ui-field__req"> (required)</span>}
      </label>
      {hint && (
        <div id={hintId} className="ui-field__hint">
          {hint}
        </div>
      )}
      {children({ id, describedBy, invalid: Boolean(error) })}
      {error && (
        <div id={errId} className="ui-field__error" role="alert">
          <AlertTriangle size={16} aria-hidden="true" /> {error}
        </div>
      )}
    </div>
  );
}

export interface SelectProps extends Omit<SelectHTMLAttributes<HTMLSelectElement>, 'children'> {
  label: string;
  options: { value: string; label: string }[];
  hint?: ReactNode;
  error?: string | null;
}

export function Select({ label, options, hint, error, ...rest }: SelectProps) {
  return (
    <Field label={label} hint={hint} error={error}>
      {({ id, describedBy, invalid }) => (
        <select {...rest} id={id} aria-describedby={describedBy} aria-invalid={invalid || undefined} className="ui-select">
          {options.map((o) => (
            <option key={o.value} value={o.value}>
              {o.label}
            </option>
          ))}
        </select>
      )}
    </Field>
  );
}

// --- Tabs (WAI-ARIA tabs with automatic activation and roving focus) -------------------------------------------------

export interface TabDef {
  id: string;
  label: string;
  count?: number;
}

/** `id` is shared with tabPanelProps(id, tab) so each tab controls a panel that exists (WAI-ARIA, axe). */
export function Tabs({ id: baseId, tabs, active, onChange, label }: { id: string; tabs: TabDef[]; active: string; onChange: (id: string) => void; label: string }) {
  const refs = useRef<(HTMLButtonElement | null)[]>([]);
  const onKey = (e: KeyboardEvent, i: number) => {
    const last = tabs.length - 1;
    const next = e.key === 'ArrowRight' ? (i === last ? 0 : i + 1) : e.key === 'ArrowLeft' ? (i === 0 ? last : i - 1)
      : e.key === 'Home' ? 0 : e.key === 'End' ? last : null;
    if (next === null) return;
    e.preventDefault();
    onChange(tabs[next]!.id);
    refs.current[next]?.focus();
  };
  return (
    <div role="tablist" aria-label={label} className="ui-tabs">
      {tabs.map((t, i) => (
        <button
          key={t.id}
          ref={(el) => {
            refs.current[i] = el;
          }}
          type="button"
          role="tab"
          id={`${baseId}-${t.id}`}
          aria-selected={t.id === active}
          aria-controls={`${baseId}-${t.id}-panel`}
          tabIndex={t.id === active ? 0 : -1}
          className="ui-tab"
          onClick={() => onChange(t.id)}
          onKeyDown={(e) => onKey(e, i)}
        >
          {t.label}
          {t.count !== undefined && <span className="ui-tab__count">{t.count}</span>}
        </button>
      ))}
    </div>
  );
}

export function tabPanelProps(tabsId: string, tab: string) {
  return { role: 'tabpanel', id: `${tabsId}-${tab}-panel`, 'aria-labelledby': `${tabsId}-${tab}`, tabIndex: 0 } as const;
}

// --- Status pill ------------------------------------------------------------------------------------------------------

const STATUS: Record<string, { icon: LucideIcon; tone: string; label: string }> = {
  pending: { icon: Clock, tone: 'neutral', label: 'Pending' },
  running: { icon: Loader2, tone: 'info', label: 'Running' },
  completed: { icon: CheckCircle2, tone: 'success', label: 'Completed' },
  succeeded: { icon: CheckCircle2, tone: 'success', label: 'Succeeded' },
  partial: { icon: AlertTriangle, tone: 'warn', label: 'Partial' },
  refused: { icon: Ban, tone: 'warn', label: 'Refused' },
  failed: { icon: XCircle, tone: 'danger', label: 'Failed' },
  cancelled: { icon: OctagonX, tone: 'neutral', label: 'Cancelled' },
  staged: { icon: CircleDashed, tone: 'warn', label: 'Staged (not committed)' },
  committed: { icon: CheckCircle2, tone: 'success', label: 'Committed' },
  expired: { icon: Clock, tone: 'neutral', label: 'Expired' },
};

export function StatusPill({ status, label }: { status: string; label?: string }) {
  const s = STATUS[status] ?? { icon: Info, tone: 'neutral', label: status };
  const Icon = s.icon;
  return (
    <span className={`ui-pill ui-pill--${s.tone}`} data-status={status}>
      <Icon size={14} aria-hidden="true" className={status === 'running' ? 'ui-spin' : undefined} />
      {label ?? s.label}
    </span>
  );
}

// --- Banner -----------------------------------------------------------------------------------------------------------

const BANNER: Record<string, LucideIcon> = { info: Info, warn: AlertTriangle, danger: XCircle, success: CheckCircle2 };

export function Banner({ tone = 'info', title, children, live = false, testId }: { tone?: 'info' | 'warn' | 'danger' | 'success'; title?: string; children?: ReactNode; live?: boolean; testId?: string }) {
  const Icon = BANNER[tone]!;
  return (
    <div className={`ui-banner ui-banner--${tone}`} role={live ? (tone === 'danger' ? 'alert' : 'status') : undefined} data-testid={testId}>
      <Icon size={20} aria-hidden="true" className="ui-banner__icon" />
      <div>
        {title && <strong className="ui-banner__title">{title}</strong>}
        {children && <div className="ui-banner__body">{children}</div>}
      </div>
    </div>
  );
}

// --- Dialog (native <dialog>: focus trap, Escape, inert background come from the browser) -----------------------------

export function Dialog({ open, title, onClose, children, actions }: { open: boolean; title: string; onClose: () => void; children: ReactNode; actions?: ReactNode }) {
  const ref = useRef<HTMLDialogElement>(null);
  const titleId = useId();
  useEffect(() => {
    const d = ref.current;
    if (!d) return;
    if (open && !d.open) {
      d.showModal?.();
      // Native dialogs focus their first focusable element, which is the close button in the header; put keyboard
      // users in the first field of the body instead (WCAG 2.4.3 focus order).
      d.querySelector<HTMLElement>('.ui-dialog__body :is(input, select, textarea)')?.focus();
    }
    if (!open && d.open) d.close?.();
  }, [open]);
  return (
    <dialog ref={ref} className="ui-dialog" aria-labelledby={titleId} onClose={onClose} onCancel={onClose}>
      <div className="ui-dialog__head">
        <h2 id={titleId}>{title}</h2>
        <IconButton icon={X} label="Close dialog" onClick={onClose} />
      </div>
      <div className="ui-dialog__body">{children}</div>
      {actions && <div className="ui-dialog__actions">{actions}</div>}
    </dialog>
  );
}

// --- Live region / toast ----------------------------------------------------------------------------------------------

/** Polite announcements for progress (never assertive for routine updates). */
export function LiveRegion({ message }: { message: string }) {
  return (
    <div className="visually-hidden" role="status" aria-live="polite" aria-atomic="true">
      {message}
    </div>
  );
}

export function Toast({ message, onDismiss }: { message: string | null; onDismiss: () => void }) {
  useEffect(() => {
    if (!message) return undefined;
    const t = window.setTimeout(onDismiss, 6000);
    return () => window.clearTimeout(t);
  }, [message, onDismiss]);
  if (!message) return null;
  return (
    <div className="ui-toast" role="status" aria-live="polite">
      <span>{message}</span>
      <IconButton icon={X} label="Dismiss message" onClick={onDismiss} />
    </div>
  );
}

// --- Progress ---------------------------------------------------------------------------------------------------------

export function ProgressBar({ value, max, label }: { value: number; max: number; label: string }) {
  const pct = max > 0 ? Math.round((value / max) * 100) : 0;
  return (
    <div className="ui-progress">
      <div className="ui-progress__label">
        <span>{label}</span>
        <span className="num">
          {value} / {max} ({pct}%)
        </span>
      </div>
      <div role="progressbar" aria-label={label} aria-valuemin={0} aria-valuemax={max} aria-valuenow={value} className="ui-progress__track">
        <div className="ui-progress__fill" style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}

// --- Empty state / skeleton -------------------------------------------------------------------------------------------

export function EmptyState({ icon: Icon = Info, title, children, action }: { icon?: LucideIcon; title: string; children?: ReactNode; action?: ReactNode }) {
  return (
    <div className="ui-empty">
      <Icon size={28} aria-hidden="true" />
      <p className="ui-empty__title">{title}</p>
      {children && <div className="ui-empty__body">{children}</div>}
      {action}
    </div>
  );
}

export function Skeleton({ lines = 3, label = 'Loading' }: { lines?: number; label?: string }) {
  return (
    <div className="ui-skeleton" role="status" aria-label={label}>
      {Array.from({ length: lines }, (_, i) => (
        <div key={i} className="ui-skeleton__line" style={{ width: `${90 - i * 12}%` }} />
      ))}
    </div>
  );
}

// --- Data table (sortable, paginated, stable keys) --------------------------------------------------------------------

export interface Column<T> {
  key: string;
  header: string;
  render: (row: T) => ReactNode;
  sortValue?: (row: T) => string | number;
  numeric?: boolean;
}

export function DataTable<T>({
  rows, columns, rowKey, caption, pageSize = 25, emptyText = 'Nothing to show.', onRowClick,
}: {
  rows: T[];
  columns: Column<T>[];
  rowKey: (row: T) => string;
  caption: string;
  pageSize?: number;
  emptyText?: string;
  onRowClick?: (row: T) => void;
}) {
  const [sort, setSort] = useState<{ key: string; dir: 'asc' | 'desc' } | null>(null);
  const [page, setPage] = useState(0);
  const col = sort ? columns.find((c) => c.key === sort.key) : undefined;
  const sorted = col?.sortValue
    ? [...rows].sort((a, b) => {
        const va = col.sortValue!(a);
        const vb = col.sortValue!(b);
        const d = va < vb ? -1 : va > vb ? 1 : rowKey(a).localeCompare(rowKey(b)); // stable tie-breaker
        return sort!.dir === 'asc' ? d : -d;
      })
    : rows;
  const pages = Math.max(1, Math.ceil(sorted.length / pageSize));
  const current = Math.min(page, pages - 1);
  const visible = sorted.slice(current * pageSize, current * pageSize + pageSize);
  const toggle = (key: string) => {
    setSort((s) => (s?.key === key ? { key, dir: s.dir === 'asc' ? 'desc' : 'asc' } : { key, dir: 'asc' }));
    setPage(0);
  };
  return (
    <div className="ui-table">
      <div className="ui-table__scroll">
        <table className="data">
          <caption className="visually-hidden">{caption}</caption>
          <thead>
            <tr>
              {columns.map((c) => {
                const dir = sort?.key === c.key ? sort.dir : undefined;
                const SortIcon = dir === 'asc' ? ArrowUp : dir === 'desc' ? ArrowDown : ArrowUpDown;
                return (
                  <th key={c.key} scope="col" aria-sort={dir === 'asc' ? 'ascending' : dir === 'desc' ? 'descending' : undefined} className={c.numeric ? 'num' : undefined}>
                    {c.sortValue ? (
                      <button type="button" onClick={() => toggle(c.key)}>
                        {c.header} <SortIcon size={14} aria-hidden="true" />
                      </button>
                    ) : (
                      c.header
                    )}
                  </th>
                );
              })}
            </tr>
          </thead>
          <tbody>
            {visible.length === 0 ? (
              <tr>
                <td colSpan={columns.length} className="muted">
                  {emptyText}
                </td>
              </tr>
            ) : (
              visible.map((r) => (
                <tr key={rowKey(r)} onClick={onRowClick ? () => onRowClick(r) : undefined} className={onRowClick ? 'is-clickable' : undefined}>
                  {columns.map((c) => (
                    <td key={c.key} className={c.numeric ? 'num' : undefined}>
                      {c.render(r)}
                    </td>
                  ))}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
      {pages > 1 && (
        <nav className="ui-pager" aria-label={`${caption}: pages`}>
          <IconButton icon={ChevronLeft} label="Previous page" disabled={current === 0} onClick={() => setPage(current - 1)} />
          <span className="num">
            Page {current + 1} of {pages} · {sorted.length} rows
          </span>
          <IconButton icon={ChevronRight} label="Next page" disabled={current >= pages - 1} onClick={() => setPage(current + 1)} />
        </nav>
      )}
    </div>
  );
}
