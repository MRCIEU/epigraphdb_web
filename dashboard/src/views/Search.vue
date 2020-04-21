<template>
  <div>
    <h1>Search</h1>
    <hr style="margin: 20px 0px;border: 1px solid #e3e3e3;" />
    <b-card no-body>
      <b-tabs card align="center">
        <b-tab title="Explore by meta node">
          <ExploreNode />
        </b-tab>
        <b-tab title="Explore by path">
          <ExplorePath />
        </b-tab>
      </b-tabs>
    </b-card>
  </div>
</template>

<script>
import ExploreNode from "@/components/Search/ExploreNode";
import ExplorePath from "@/components/Search/ExplorePath";

export default {
  name: "search",
  components: {
    ExploreNode,
    ExplorePath
  }
};
</script>
