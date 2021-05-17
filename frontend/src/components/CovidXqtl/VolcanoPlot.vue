<template>
  <div>
    <highcharts :options="options"></highcharts>
  </div>
</template>

<script>
import { Chart } from "highcharts-vue";

export default {
  name: "VolcanoPlot",
  components: {
    highcharts: Chart,
  },
  props: {
    graphDataInput: Object,
  },
  computed: {
    options: function() {
      if (this.graphDataInput) {
        return {
          chart: {
            type: "scatter",
            zoomType: "xy",
          },
          title: {
            text: "MR results",
          },
          subtitle: {
            text: "P-value threshold for top results: 1.1e-6",
          },
          xAxis: {
            title: {
              enabled: true,
              text: "Z-score (beta/se)",
            },
            startOnTick: true,
            endOnTick: true,
            showLastLabel: true,
          },
          yAxis: {
            title: {
              text: "-log10(pval)",
            },
          },
          credits: {
            enabled: false,
          },
          plotOptions: {
            scatter: {
              marker: {
                radius: 5,
                states: {
                  hover: {
                    enabled: true,
                    lineColor: "rgb(100,100,100)",
                  },
                },
              },
              states: {
                hover: {
                  marker: {
                    enabled: false,
                  },
                },
              },
              tooltip: {
                headerFormat: "{series.name}<br>",
                pointFormat: `exposure:<b>{point.exposure}</b>
                   <br>
                   outcome:<b>{point.outcome}</b>
                   <br>
                   tissue:<b>{point.tissue}</b>
                   <br>
                   Z-score: <b>{point.x}</b>
                   <br>
                   -log10(pval): <b>{point.y}</b>
                  `,
              },
            },
          },
          series: [
            {
              name: "Top MR associations",
              color: "rgba(238, 83, 80, .8)",
              data: this.graphDataInput.top_results,
            },
            {
              name: "Other MR associations",
              color: "rgba(51, 122, 183, .8)",
              data: this.graphDataInput.other_results,
              turboThreshold: 2000,
            },
          ],
        };
      } else {
        return null;
      }
    },
  },
};
</script>
