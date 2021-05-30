<template>
  <div>
    <b-tabs>
      <b-tab title="Metrics for nodes">
        <Table v-if="schemaNodesData" :table-data-input="schemaNodesData">
          <template #cell(node_name)="data">
            <MetaNode
              :meta-node="data.item.node_name.name"
              :url="data.item.node_name.url"
              no-code-bg
            />
          </template>
        </Table>
      </b-tab>
      <b-tab title="Metrics for relationships">
        <Table v-if="schemaRelsData" :table-data-input="schemaRelsData">
          <template #cell(relationshipType)="data">
            <MetaRel
              :meta-rel="data.item.relationshipType.name"
              :url="data.item.relationshipType.url"
              no-code-bg
            />
          </template>
        </Table>
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>
import axios from "axios";

import MetaNode from "@/components/miscs/DecoratedMetaNode";
import MetaRel from "@/components/miscs/DecoratedMetaRel";
import Table from "@/components/Utils/TableGeneric1";
const config = require("@/config");

export default {
  name: "Metrics",
  components: {
    MetaNode,
    MetaRel,
    Table,
  },
  data: () => ({
    schemaData: null,
  }),
  methods: {
    getAboutSchemaData() {
      const url = `${config.web_backend_url}/about/metrics`;
      axios.get(url).then(response => {
        this.schemaData = response.data;
      });
    },
  },
  mounted: function() {
    this.getAboutSchemaData();
  },
  computed: {
    schemaNodesData() {
      return this.schemaData
        ? {
            items: this.schemaData.meta_node,
            fields: [
              {
                key: "node_name",
                label: "Meta node",
                sortable: true,
              },
              {
                key: "count",
                label: "count",
                sortable: true,
                formatter: value => {
                  return value.toLocaleString();
                },
              },
            ],
          }
        : null;
    },
    schemaRelsData() {
      return this.schemaData
        ? {
            items: this.schemaData.meta_rel,
            fields: [
              {
                key: "relationshipType",
                label: "Meta relationship",
                sortable: true,
              },
              {
                key: "count",
                label: "count",
                sortable: true,
                formatter: value => {
                  return value.toLocaleString();
                },
              },
            ],
          }
        : null;
    },
  },
};
</script>
