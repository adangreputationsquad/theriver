class IDAddPlotModal:
    id = "add_plot_modal"
    body = "modal_body_add_plot"
    dropdown_views = "select_view_dropdown_plot"
    dropdown_plots_div = "select_plot_dropdown_div"
    dropdown_plots = "select_plot_dropdown"
    validate_button = "validate_add_plot"
    config_panel_div = "plot_args_div"
    preview = "add_plot_view_preview"


class IDAddViewModal:
    id = "add_view_modal"
    body = "modal_body_add_view"
    dropdown_views = "select_view_dropdown_view"
    validate_button = "validate_add_view"
    preview = "view_modal_view_preview"


class IDMainDashboard:
    download_button = "download_button"
    add_plot_button = "add_plot_button"
    add_view_button = "add_view_button"
    canvas = "canvas"


class IDPlots:
    pass


class IDs:
    add_plot_modal = IDAddPlotModal
    add_view_modal = IDAddViewModal
    main_dashboard = IDMainDashboard
    plots = IDPlots
