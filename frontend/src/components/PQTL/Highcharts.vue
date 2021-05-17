<template>
  <div>
    <highcharts :options="options"></highcharts>
  </div>
</template>

<script>
import { Chart } from "highcharts-vue";

export default {
  name: "Highcharts",
  components: {
    highcharts: Chart,
  },
  props: {
    graphDataInput: Object,
    query: String,
  },
  computed: {
    options: function() {
      if (this.query && this.graphDataInput) {
        return {
          chart: {
            type: "scatter",
            zoomType: "xy",
          },
          title: {
            text: `Mendelian Randomization results for ${this.query}`,
          },
          xAxis: {
            title: {
              enabled: true,
              text:
                "Z-value (beta/standard error) per SD unit in plasma protein",
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
                headerFormat: "<b>{series.name}</b><br>",
                pointFormat:
                  "{point.name}<br> {point.x} (Z-value), {point.y} (-log10(pvalue))",
              },
            },
          },
          series: [
            {
              name: "Top MR associations",
              color: "rgba(223, 83, 83, .5)",
              data: this.graphDataInput.plot_output.topres,
            },
            {
              name: "Other MR associations",
              color: "rgba(119, 152, 191, .5)",
              data: this.graphDataInput.plot_output.otherres,
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
