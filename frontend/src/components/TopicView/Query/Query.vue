<template>
  <div>
    <div class="network-plot-content">
      <b-row v-if="queryDiagramData">
        <b-col cols="4"
          ><h4>
            <span v-b-tooltip.hover :title="tooltipDoc.query.cypher_diagram"
              >Cypher diagram</span
            >
          </h4></b-col
        >
        <b-col>
          <QueryDiagram :diagram-data="queryDiagramData" />
        </b-col>
      </b-row>
      <b-row v-if="resQueryCypher">
        <b-col cols="4"
          ><h4>
            <span v-b-tooltip.hover :title="tooltipDoc.query.cypher_query"
              >Cypher query</span
            >
          </h4></b-col
        >
        <b-col cols="8" class="wrap">
          <CypherQuery :cypher-query="resQueryCypher" />
        </b-col>
      </b-row>
    </div>
    <b-row v-if="resQueryCurl">
      <b-col cols="4"
        ><h4>
          <span v-b-tooltip.hover :title="tooltipDoc.query.api_call"
            >API call</span
          >
        </h4></b-col
      >
      <b-col cols="8" class="wrap">
        <ApiCall
          :api-call-data="resQueryCurl"
          :snippet-request="resQuerySnippetRequest"
          :snippet-r-pkg="resQuerySnippetRPkg"
        />
      </b-col>
    </b-row>
    <b-row v-if="resQueryResponsePreview">
      <b-col cols="4"
        ><h4>
          <span v-b-tooltip.hover :title="tooltipDoc.query.preview"
            >Response data preview</span
          >
        </h4></b-col
      >
      <b-col>
        <ResponseData :response-data="resQueryResponsePreview" />
      </b-col>
    </b-row>
  </div>
</template>

<script>
import QueryDiagram from "@/components/TopicView/Query/Diagram.vue";
import CypherQuery from "@/components/TopicView/Query/CypherQuery.vue";
import ApiCall from "@/components/TopicView/Query/ApiCall.vue";
import ResponseData from "@/components/TopicView/Query/ResponseData.vue";
import tooltips from "@/assets/docs/hover-tooltips";

export default {
  name: "Query",
  components: {
    QueryDiagram,
    CypherQuery,
    ApiCall,
    ResponseData
  },
  data: () => ({
    tooltipDoc: tooltips
  }),
  props: {
    queryData: Object,
    queryDiagramData: Object
  },
  computed: {
    resQueryCypher: function() {
      return this.queryData ? this.queryData.cypher : null;
    },
    resQueryCurl: function() {
      return this.queryData ? this.queryData.curl : null;
    },
    resQuerySnippetRequest: function() {
      return this.queryData ? this.queryData.api_snippet : null;
    },
    resQuerySnippetRPkg: function() {
      return this.queryData ? this.queryData.r_pkg_snippet : null;
    },
    resQueryResponsePreview: function() {
      return this.queryData ? this.queryData.response_data : null;
    }
  }
};
</script>
