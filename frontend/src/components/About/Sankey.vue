<template>
  <div>
    <highcharts
      id="container"
      :options="options"
      v-if="rescaledData"
    ></highcharts>
  </div>
</template>

<style>
#container {
  height: 1000px;
}
</style>

<script>
import _ from "lodash";

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
    highcharts: Chart,
  },
  computed: {
    rescaledData() {
      return _.map(data, function(item) {
        if (item.weight) {
          return {
            color: item.color ? item.color : null,
            from: item.from,
            to: item.to,
            // HACK
            weight: 1,
            count: item.count,
          };
        } else {
          return {
            color: item.color ? item.color : null,
            from: item.from,
            to: item.to,
            // HACK
            weight: null,
            count: item.count,
          };
        }
      });
    },
    options() {
      return {
        title: {
          text: null,
        },
        accessibility: {
          point: {
            valueDescriptionFormat:
              "{index}. From {point.from} to {point.to}: {point.count}.",
          },
        },
        series: [
          {
            keys: ["from", "to", "weight", "name"],
            linkOpacity: 1,
            data: this.rescaledData,
            type: "sankey",
            name: "Data relationship",
            dataLabels: {
              color: "#333",
              style: {
                fontSzie: "10px",
              },
              allowOverlap: true,
            },
            colors: ["lightblue"],
          },
        ],
        tooltip: {
          formatter: function() {
            if (this.point.formatPrefix == "point") {
              let count = this.point.count;
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
                sum = sum + this.point.linksTo[i].count;
              }
              for (i in this.point.linksFrom) {
                sum = sum + this.point.linksFrom[i].count;
              }
              return this.point.id + ": " + parseInt(sum).toLocaleString();
            }
          },
        },
      };
    },
  },
};
</script>
