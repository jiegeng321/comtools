#-*-coding:utf-8-*-
from flask import Flask, render_template
import numpy as np
import pandas as pd

from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line
from pyecharts.globals import ThemeType
from pyecharts.commons.utils import JsCode
#from pyecharts import Overlap

app = Flask(__name__, static_folder="static")
app.jinja_env.auto_reload = True
app.config["TEMPLATES_AUTO_RELOAD"] = True

def get_porn_model_metric_graph():
    porn_pr = pd.read_csv("metrics/porn_pr.csv")
    porn_label = pd.read_csv("metrics/porn_labels.csv")

    porn_pr_bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
        .add_xaxis(porn_pr.version.tolist())
        .add_yaxis("召回率", porn_pr.recall.tolist())
        .add_yaxis("查准率", porn_pr.precision.tolist())
        .set_global_opts(
            title_opts=opts.TitleOpts(title="鉴黄模型准召率", pos_left='left'),
            legend_opts=opts.LegendOpts(is_show=True, pos_left='25%'),
            toolbox_opts=opts.ToolboxOpts(orient="vertical", pos_left="95%"),
        )
    )

    porn_label_bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
        .add_xaxis(porn_label.version.tolist())
        .add_yaxis("标签数量", porn_label.label.tolist())
        .set_global_opts(
            title_opts=opts.TitleOpts(title="鉴黄模型标签数量", pos_left='50%'),
            legend_opts=opts.LegendOpts(is_show=True, pos_left='75%'),
            toolbox_opts=opts.ToolboxOpts(orient="vertical", pos_left="95%"),
        )
    )
    grid = Grid()
    grid.add(porn_pr_bar, grid_opts=opts.GridOpts(
        pos_left='5%', pos_right='55%'))
    grid.add(porn_label_bar, grid_opts=opts.GridOpts(
        pos_left='50%', pos_right='5%'))
    return grid

def get_porn_fine_model_metric_graph():
    porn_pr = pd.read_csv("metrics/porn_fine_pr.csv")
    porn_label = pd.read_csv("metrics/porn_fine_labels.csv")

    porn_pr_bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
        .add_xaxis(porn_pr.version.tolist())
        .add_yaxis("召回率", porn_pr.recall.tolist())
        .add_yaxis("查准率", porn_pr.precision.tolist())
        .set_global_opts(
            title_opts=opts.TitleOpts(title="鉴黄模型准召率", pos_left='left'),
            legend_opts=opts.LegendOpts(is_show=True, pos_left='25%'),
            toolbox_opts=opts.ToolboxOpts(orient="vertical", pos_left="95%"),
        )
    )

    porn_label_bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
        .add_xaxis(porn_label.version.tolist())
        .add_yaxis("标签数量", porn_label.label.tolist())
        .set_global_opts(
            title_opts=opts.TitleOpts(title="鉴黄模型标签数量", pos_left='50%'),
            legend_opts=opts.LegendOpts(is_show=True, pos_left='75%'),
            toolbox_opts=opts.ToolboxOpts(orient="vertical", pos_left="95%"),
        )
    )
    grid = Grid()
    grid.add(porn_pr_bar, grid_opts=opts.GridOpts(
        pos_left='5%', pos_right='55%'))
    grid.add(porn_label_bar, grid_opts=opts.GridOpts(
        pos_left='50%', pos_right='5%'))
    return grid


def get_terror_cls_model_metric_graph():
    terror_cls_pr = pd.read_csv("metrics/terror_cls_pr.csv")
    terror_cls_label = pd.read_csv("metrics/terror_cls_labels.csv")

    terror_cls_pr_bar = (
        Bar()
        .add_xaxis(terror_cls_pr.version.tolist())
        .add_yaxis("召回率",  terror_cls_pr.recall.tolist())
        .add_yaxis("查准率",  terror_cls_pr.precision.tolist())
        .set_global_opts(
            title_opts=opts.TitleOpts(title="暴恐分类模型准召率", pos_left='left'),
            legend_opts=opts.LegendOpts(is_show=True, pos_left='25%'),
            toolbox_opts=opts.ToolboxOpts(orient="vertical", pos_left="95%"),
        )
        .set_series_opts(
            label_opts=opts.LabelOpts(
                formatter=JsCode(
                    '''function(params) {return Number(params.value).toFixed(2);}''')
            )
        )
    )
    terror_cls_label_bar = (
        Bar()
        .add_xaxis(terror_cls_label.version.tolist())
        .add_yaxis("标签数量", terror_cls_label.label.tolist())
        .set_global_opts(
            title_opts=opts.TitleOpts(title="暴恐分类模型标签数量", pos_left='50%'),
            legend_opts=opts.LegendOpts(is_show=True, pos_left='75%'),
            toolbox_opts=opts.ToolboxOpts(orient="vertical", pos_left="95%"),
        )
    )
    grid = Grid()
    grid.add(terror_cls_pr_bar, grid_opts=opts.GridOpts(
        pos_left='5%', pos_right='55%'))
    grid.add(terror_cls_label_bar, grid_opts=opts.GridOpts(
        pos_left='50%', pos_right='5%'))
    return grid



def get_terror_det_model_metric_graph():
    terror_det_pr = pd.read_csv("metrics/terror_det_tpr_fpr.csv",index_col=0)
    terror_det_label = pd.read_csv("metrics/terror_det_labels.csv")
    show_acc = pd.DataFrame(index=terror_det_pr.index)
    version = [v for v in terror_det_pr.index.tolist()]
    version_date = ["{} \n{}".format(v, terror_det_pr['date'][v]) for v in version]

    terror_det_pr_bar = (
        Bar()
        .add_xaxis(version_date)
        .add_yaxis("召回率",  terror_det_pr.tpr.tolist())
        .add_yaxis("误检率",  terror_det_pr.fpr.tolist())
        .set_global_opts(
            title_opts=opts.TitleOpts(title="暴恐检测模型召回率误检率", pos_left='left'),
            legend_opts=opts.LegendOpts(is_show=True, pos_left='25%'),
            toolbox_opts=opts.ToolboxOpts(orient="vertical", pos_left="95%"),
            xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate": 45, "fontSize": 8})

        )
        .set_series_opts(
            label_opts=opts.LabelOpts(
                formatter=JsCode(
                    '''function(params) {return Number(params.value).toFixed(3);}''')
            )
        )
    )
    terror_det_label_bar = (
        Bar()
        .add_xaxis(version_date)
        .add_yaxis("标签数量", terror_det_label.label.tolist())
        .set_global_opts(
            title_opts=opts.TitleOpts(title="暴恐检测模型标签数量及QPS", pos_left='50%'),
            legend_opts=opts.LegendOpts(is_show=True, pos_left='75%'),
            toolbox_opts=opts.ToolboxOpts(orient="vertical", pos_left="95%"),
	    xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate": 45, "fontSize": 8})
        )
    )

    terror_det_qps_line = (
        Line()
        .add_xaxis(version_date)
        .add_yaxis("QPS", terror_det_pr.qps.tolist())
        .set_global_opts(
            title_opts=opts.TitleOpts(pos_left='10%'),
            legend_opts=opts.LegendOpts(is_show=True, pos_right='11%'),
            toolbox_opts=opts.ToolboxOpts(orient="vertical", pos_right="10%"),
            xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate": 45, "fontSize": 8})
        )
        .set_series_opts(color="black",)
    )



    grid = Grid()
    grid.add(terror_det_pr_bar, grid_opts=opts.GridOpts(
         pos_right='60%'))
    grid.add(terror_det_label_bar, grid_opts=opts.GridOpts(
         pos_bottom='60%', pos_left='60%'))
    grid.add(terror_det_qps_line, grid_opts=opts.GridOpts(
         pos_top='60%', pos_left='60%'))
  

    return grid


def get_ocr_model_metric_graph(file_path='metrics/ai-adver-ocr-metric.csv'):

    df = pd.read_csv(file_path, index_col=0)

    used_datasets = ['AD964', 'AD964ROT', 'RB500']
    weights = {'AD964': 0.45546256, 'AD964ROT': 0.45546256, 'RB500': 0.08907488}

    # get acc
    show_acc = pd.DataFrame(index=df.index)
    for d in used_datasets:
        show_acc['LR_'+d] = df['LR_'+d] * weights[d]
    show_acc = show_acc.sum(axis=1) * 100
    show_acc = show_acc.round(2)

    # version list
    competitions = ['百度通用', '百度高精', '达摩院']
    version = [v for v in df.index.tolist() if v not in competitions]

    # date list
    show_version = ["{} \n{}".format(v, df['DATE'][v]) for v in version]

    # get qps
    show_qps = df['QPS']

    acc_bar = (
        Bar()
        .add_xaxis(show_version)
        .add_yaxis("行召回",  show_acc[version].tolist())
        .set_global_opts(
            title_opts=opts.TitleOpts(pos_left='left'),
            legend_opts=opts.LegendOpts(is_show=True, pos_left='25%'),
            toolbox_opts=opts.ToolboxOpts(orient="vertical", pos_left="95%"),
            xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate": 45, "fontSize": 8}),
        )
        .set_series_opts(
            color="#FF5809",
            label_opts=opts.LabelOpts(
                formatter=JsCode('''function(params) {return Number(params.value).toFixed(2);}'''),
            ),
            markline_opts=opts.MarkLineOpts(
                # 标记线数据
                data=[ opts.MarkLineItem(name=n, y=show_acc[n]) for n in competitions],
                # 图形是否不响应和触发鼠标事件，默认为 false，即响应和触发鼠标事件。
                is_silent=False,

                # 也可以在这里设置标线两端的标记类型，可以是一个数组分别指定两端，也可以是单个统一指定，具体格式见 data.symbol。
                symbol='none',

                # 标签配置项，参考 `series_options.LabelOpts`
                # label_opts=opts.LabelOpts(
                #     is_show=True,
                #     position='end',
                #     font_size=10,
                #     formatter="{value}.baidu"
                # ),

                # 标记线样式配置项，参考 `series_options.LineStyleOpts`
                linestyle_opts=opts.LineStyleOpts(
                    is_show=True,
                    width=1,
                    type_="dashed",
                    color="#2a5caa"
                )

            ),
        )

    )

    qps_line = (
        Line()
        .add_xaxis(show_version)
        .add_yaxis("QPS", show_qps[version].tolist())
        .set_global_opts(
            title_opts=opts.TitleOpts(pos_left='50'),
            legend_opts=opts.LegendOpts(is_show=True, pos_left='75%'),
            toolbox_opts=opts.ToolboxOpts(orient="vertical", pos_left="95%"),
            xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate": 45, "fontSize": 8})
        )
        .set_series_opts(color="black",)
    )



    grid = Grid()
    grid.add(acc_bar, grid_opts=opts.GridOpts(
        pos_left='5%', pos_right='55%'))
    grid.add(qps_line, grid_opts=opts.GridOpts(
        pos_left='60%', pos_right='5%'))
    return grid

def get_blacklist_model_metric_graph():
    blacklist_pr = pd.read_csv("metrics/blacklist-gen_pr.csv")
    blacklist_fp = pd.read_csv("metrics/blacklist-gen_fp.csv")

    blacklist_pr_bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
        .add_xaxis(blacklist_pr.version.tolist())
        .add_yaxis("召回率", blacklist_pr.recall.tolist())
        .add_yaxis("查准率", blacklist_pr.precision.tolist())
        .set_global_opts(
            title_opts=opts.TitleOpts(title="黑样本库准召率", pos_left='left'),
            legend_opts=opts.LegendOpts(is_show=True, pos_left='25%'),
            toolbox_opts=opts.ToolboxOpts(orient="vertical", pos_left="95%"),
        )
    )

    blacklist_label_bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
        .add_xaxis(blacklist_fp.version.tolist())
        .add_yaxis("误检率", blacklist_fp.fp.tolist())
        .set_global_opts(
            title_opts=opts.TitleOpts(title="黑样本库误检率", pos_left='50%'),
            legend_opts=opts.LegendOpts(is_show=True, pos_left='75%'),
            toolbox_opts=opts.ToolboxOpts(orient="vertical", pos_left="95%"),
        )
    )
    grid = Grid()
    grid.add(blacklist_pr_bar, grid_opts=opts.GridOpts(
        pos_left='5%', pos_right='55%'))
    grid.add(blacklist_label_bar, grid_opts=opts.GridOpts(
        pos_left='50%', pos_right='5%'))
    return grid




@app.route("/")
def index():
    porn_grid = get_porn_model_metric_graph()
    porn_fine_grid = get_porn_fine_model_metric_graph()
    terror_cls_grid = get_terror_cls_model_metric_graph()
    terror_det_grid = get_terror_det_model_metric_graph()
    ocr_grid = get_ocr_model_metric_graph('metrics/ai-adver-ocr-metric.csv')
    ocr_acc_grid = get_ocr_model_metric_graph('metrics/ai-adver-ocr-acc-metric.csv')
    blacklist_grid = get_blacklist_model_metric_graph()
    return render_template(
        "index.html",
        porn_metrics=porn_grid.dump_options(),
        porn_fine_metrics=porn_fine_grid.dump_options(),
        terror_cls_metrics=terror_cls_grid.dump_options(),
        terror_det_metrics =terror_det_grid.dump_options(),
        ocr_metrics=ocr_grid.dump_options(),
        ocr_acc_metrics=ocr_acc_grid.dump_options(),
        blacklist_metrics=blacklist_grid.dump_options(),
    )


if __name__ == "__main__":
    app.run()
