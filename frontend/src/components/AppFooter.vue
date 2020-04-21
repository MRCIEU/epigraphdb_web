<template>
  <footer class="blue">
    <b-container>
      <b-row class="page-footer">
        <b-col>
          <h5 class="text-uppercase">EpiGraphDB, developed at the MRC IEU</h5>
          <p>
            MRC Integrative Epidemiology Unit, University of Bristol<br />
            Oakfield House, Oakfield Grove<br />
            Clifton, Bristol, UK<br />
            BS8 2BN.<br /><br />
          </p>
        </b-col>
        <b-col cols="12" md="auto"></b-col>
        <b-col col lg="4">
          <!-- Links -->
          <h5 class="text-uppercase">Key links</h5>

          <ul class="list-unstyled">
            <li>
              <a href="http://www.biocompute.org.uk/"
                >IEU data mining programme</a
              >
            </li>
            <li>
              <a href="http://www.bristol.ac.uk/integrative-epidemiology/"
                >MRC Integrative Epidemiology Unit</a
              >
            </li>
            <li>
              Email:
              <a href="mailto:feedback@epigraphdb.org"
                >feedback@epigraphdb.org</a
              >
            </li>
          </ul>
        </b-col>
      </b-row>
    </b-container>

    <!-- Copyright -->
    <div class="footer-copyright text-center">
      © 2018 - 2020 Copyright:
      <a href="http://www.bristol.ac.uk/intergrative-epidemiology/">
        MRC Integrative Epidemiology Unit, University of Bristol</a
      >
    </div>
    <!-- Copyright -->
  </footer>
</template>

<style scoped>
.footer {
  /* background-color: #f5f5f5; */
}
.footer-copyright {
  position: fixed;
  left: 0;
  bottom: 0;
  width: 100%;
  background-color: #337ab7;
  color: white;
  text-align: center;
}
.footer-copyright a {
  color: white;
}
.page-footer {
  position: relative;
  left: 0;
  bottom: 0;
  width: 100%;
  border-top: 1px solid #9cc2e3;
  padding-top: 1rem;
}
</style>
