import reflex as rx

from manufacturing_dashboard.states.dashboard_state import DashboardState


def time_completion_circle() -> rx.Component:
    """Renders the circular progress indicator for time to completion."""
    radius = 40
    return rx.el.svg(
        rx.el.circle(
            cx="50",
            cy="50",
            r=str(radius),
            stroke="#334155",
            stroke_width="8",
            fill="none",
            class_name="text-slate-700",
        ),
        rx.el.circle(
            cx="50",
            cy="50",
            r=str(radius),
            stroke="#06b6d4",
            stroke_width="8",
            fill="none",
            stroke_dasharray=DashboardState.get_time_stroke_dasharray,
            stroke_linecap="round",
            transform="rotate(-90 50 50)",
            class_name="transition-all duration-300 ease-linear",
        ),
        rx.el.text(
            DashboardState.time_to_completion.to(int).to_string() + "%",
            x="50",
            y="50",
            text_anchor="middle",
            dominant_baseline="middle",
            font_size="18",
            font_weight="bold",
            fill="#cbd5e1",
        ),
        view_box="0 0 100 100",
        class_name="w-28 h-28 mx-auto",
    )


def specification_item(label: str, value: rx.Var[str | float]) -> rx.Component:
    """Renders a single specification item row."""
    return rx.el.div(
        rx.el.span(label, class_name="text-slate-400 text-sm"),
        rx.el.span(
            value.to_string(),
            class_name="text-slate-200 text-sm font-mono",
        ),
        class_name="flex justify-between items-center py-1.5 px-3 rounded bg-slate-700/50",
    )


def sidebar() -> rx.Component:
    """Renders the sidebar component."""
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.img(
                    src="/favicon.ico",
                    alt="Company Logo",
                    class_name="h-8 w-auto mr-3",
                ),
                rx.el.span(
                    "Process Monitor",
                    class_name="text-xl font-bold text-white whitespace-nowrap",
                ),
                class_name="flex items-center justify-center h-16 border-b border-slate-700",
            ),
            rx.el.div(
                rx.el.h3(
                    "Operator Info",
                    class_name="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3 px-4",
                ),
                rx.el.div(
                    rx.el.span(
                        "Operator ID:",
                        class_name="text-slate-400",
                    ),
                    rx.el.span(
                        DashboardState.operator_id,
                        class_name="font-mono text-cyan-400",
                    ),
                    class_name="flex justify-between text-sm mb-3 px-4",
                ),
                rx.el.h3(
                    "Process Status",
                    class_name="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3 px-4",
                ),
                time_completion_circle(),
                rx.el.p(
                    rx.cond(
                        DashboardState.is_running,
                        "Process Running...",
                        "Process Idle",
                    ),
                    class_name="text-center text-sm text-slate-400 mt-2 mb-4",
                ),
                rx.el.h3(
                    "Control Limits",
                    class_name="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3 px-4",
                ),
                rx.el.div(
                    specification_item("USL", DashboardState.usl),
                    specification_item("UCL", DashboardState.ucl),
                    specification_item("Target", DashboardState.target_mean),
                    specification_item("LCL", DashboardState.lcl),
                    specification_item("LSL", DashboardState.lsl),
                    class_name="space-y-1 px-4",
                ),
                class_name="mb-6 py-6",
            ),
            class_name="flex flex-col h-full",
        ),
        class_name="hidden lg:block w-64 bg-slate-800 text-slate-200 fixed top-0 left-0 h-full border-r border-slate-700 shadow-lg z-10",
    )
