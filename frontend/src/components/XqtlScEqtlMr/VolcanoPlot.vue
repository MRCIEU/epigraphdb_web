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
    graphDataInput: Array,
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
                pointFormat: `gene:<b>{point.gene}</b>
                   <br>
                   outcome:<b>{point.outcome}</b>
                   <br>
                   cell_type: <b>{point.cell_type}</b>
                   <br>
                   activation_time:<b>{point.activation_time}</b>
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
              name: "MR associations",
              color: "rgba(51, 122, 183, .8)",
              data: this.graphDataInput,
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
