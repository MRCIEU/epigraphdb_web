<template>
  <div>
    <highcharts id="container" :options="options"></highcharts>
  </div>
</template>

<style>
#container {
  height: 1000px;
}
</style>

<script>
import Highcharts from "highcharts";
import Sankey from "highcharts/modules/sankey";
import Accessibility from "highcharts/modules/accessibility";
import { Chart } from "highcharts-vue";

Sankey(Highcharts);
Accessibility(Highcharts);

import data from "@/assets/schema/sankey-graph-data.json";

export default {
  name: "Sankey",
  components: {
    highcharts: Chart
  },
  data: () => ({
    options: {
      title: {
        text: null
      },
      accessibility: {
        point: {
          valueDescriptionFormat:
            "{index}. From {point.from} to {point.to}: {point.weight}."
        }
      },
      series: [
        {
          keys: ["from", "to", "weight", "name"],
          linkOpacity: 1,
          data: data,
          type: "sankey",
          name: "Data relationship",
          dataLabels: {
            color: "#333",
            style: {
              fontSzie: "10px"
            },
            allowOverlap: true
          },
          colors: ["lightblue"]
        }
      ],
      tooltip: {
        formatter: function() {
          if (this.point.formatPrefix == "point") {
            let count = Math.round(Math.pow(10, this.point.weight));
            return (
              this.point.from +
              "->" +
              this.point.to +
              ": " +
              parseInt(count).toLocaleString()
            );
          } else {
            var sum = 0;
            var i;
            for (i in this.point.linksTo) {
              sum =
                sum + Math.round(Math.pow(10, this.point.linksTo[i].weight));
            }
            for (i in this.point.linksFrom) {
              sum =
                sum + Math.round(Math.pow(10, this.point.linksFrom[i].weight));
            }
            return this.point.id + ": " + parseInt(sum).toLocaleString();
          }
        }
      }
    }
  })
};
</script>
