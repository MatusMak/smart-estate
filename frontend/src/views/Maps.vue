<template>
    <div>

        <base-header type="gradient-success" class="pb-6 pb-8 pt-5 pt-md-8">
        </base-header>

        <div class="container-fluid mt--7">
            <div class="row">
                <div class="col-6">
                    <div class="card shadow border-0">
                        <div id="map-canvas" class="map-canvas" data-lat="40.748817" data-lng="-73.985428" style="height: 400px;"></div>
                    </div>
                </div>
                <div v-if="place != null" class="col-6">
                  <tabs fill class="flex-column flex-md-row">
                    <card shadow>
                        <tab-pane>
                            <span slot="title">
                                <i class="ni ni-satisfied"></i>
                                Summary
                            </span>
                            <div class="description">
                              <h1>Summary:
                                <badge v-if="place.summary.grade == 'good'" type="success">Good</badge>
                                <badge v-if="place.summary.grade == 'okay'" type="warning">Okay</badge>
                                <badge v-if="place.summary.grade == 'bad'" type="danger">Bad</badge>
                                <span class="small">&nbsp;({{ place.summary.score.toFixed(2) }} %)</span>
                              </h1>

                              <div class="card shadow">
                                <div class="table-responsive">
                                  <base-table class="table align-items-center table-flush"
                                              tbody-classes="list"
                                              :data="place.categories">
                                    <template slot="columns">
                                      <th>Category</th>
                                      <th>Grade</th>
                                      <th>Score</th>
                                    </template>

                                    <template slot-scope="{row}">
                                      <td>
                                        <i :class="row.icon"></i>
                                        {{ row.title }}
                                      </td>
                                      <td>
                                        <badge v-if="row.summary.grade == 'good'" type="success">Good</badge>
                                        <badge v-if="row.summary.grade == 'okay'" type="warning">Okay</badge>
                                        <badge v-if="row.summary.grade == 'bad'" type="danger">Bad</badge>
                                      </td>
                                      <td>{{ row.summary.score.toFixed(2) }} %</td>
                                    </template>

                                  </base-table>
                                </div>
                              </div>
                            </div>
                        </tab-pane>

                        <tab-pane v-for="category in place.categories" :title="category.title">
                            <span slot="title">
                                <i :class="category.icon"></i>
                                {{ category.title }}
                            </span>
                            <div class="description">
                              <h1>{{ category.title }}:
                                <badge v-if="category.summary.grade == 'good'" type="success">Good</badge>
                                <badge v-if="category.summary.grade == 'okay'" type="warning">Okay</badge>
                                <badge v-if="category.summary.grade == 'bad'" type="danger">Bad</badge>
                                <span class="small">&nbsp;({{ category.summary.score.toFixed(2) }} %)</span>
                              </h1>

                              <div class="card shadow">
                                <div class="table-responsive">
                                  <base-table class="table align-items-center table-flush"
                                              tbody-classes="list"
                                              :data="category.providers">
                                    <template slot="columns">
                                      <th>Provider</th>
                                      <th>Grade</th>
                                      <th>Score</th>
                                      <th>Details</th>
                                    </template>

                                    <template slot-scope="{row}">
                                      <td>
                                        <i :class="row.icon"></i>
                                        {{ row.title }}
                                      </td>
                                      <td>
                                        <badge v-if="row.summary.grade == 'good'" type="success">Good</badge>
                                        <badge v-if="row.summary.grade == 'okay'" type="warning">Okay</badge>
                                        <badge v-if="row.summary.grade == 'bad'" type="danger">Bad</badge>
                                      </td>
                                      <td>{{ row.summary.score.toFixed(2) }} %</td>
                                      <td>
                                        <base-button v-if="row.data != null" type="primary" size="sm" @click="displayDetails(row)">
                                          Details
                                        </base-button>
                                      </td>

                                    </template>

                                  </base-table>
                                </div>
                              </div>
                            </div>
                        </tab-pane>
                    </card>
                  </tabs>
                </div>
                <div v-else class="col-6 loading-indicator">
                  <i class="fas fa-spinner fa-pulse"></i>
                </div>

                <div class="col-12">
                 <modal :show.sync="detailsModal.shown">
                   <template slot="header">
                      <h5 v-if="detailsModal.provider != null" class="modal-title" id="exampleModalLabel">{{ detailsModal.provider.title }}</h5>
                   </template>
                   <div>
                      <!-- PARKING AVAILABILITY -->
                      <div v-if="detailsModal.provider != null && detailsModal.provider.id == 'parking-availability'" class="table-responsive">
                        <base-table class="table align-items-center table-flush"
                                    tbody-classes="list"
                                    :data="detailsModal.provider.data">
                          <template slot="columns">
                            <th>Time slot</th>
                            <th>Capacity</th>
                            <th>Average Free</th>
                          </template>

                          <template slot-scope="{row}">
                            <td><strong>{{ row.title }}</strong></td>
                            <td>{{ row.capacity }}</td>
                            <td>{{ row.absolute }} ({{ row.relative.toFixed(2) }} %)</td>
                          </template>

                        </base-table>
                      </div>


                      <!-- PARKING PLACES -->
                      <div v-if="detailsModal.provider != null && detailsModal.provider.id == 'parking-places'" class="table-responsive">
                        <base-table class="table align-items-center table-flush"
                                    tbody-classes="list"
                                    :data="detailsModal.provider.data">
                          <template slot="columns">
                            <th>Address</th>
                            <th>Type</th>
                            <th>Capacity</th>
                          </template>

                          <template slot-scope="{row}">
                            <td><strong>{{ row.address }}</strong></td>
                            <td>{{ row.type }}</td>
                            <td>{{ row.capacity }}</td>
                          </template>

                        </base-table>
                      </div>


                      <!-- AIR CONDITIONING -->
                      <div v-if="detailsModal.provider != null && detailsModal.provider.id == 'aircondition'" class="table-responsive">
                        <base-table class="table align-items-center table-flush"
                                    tbody-classes="list"
                                    :data="detailsModal.provider.data">
                          <template slot="columns">
                            <th>Gas</th>
                            <th>Level</th>
                            <th>Score</th>
                          </template>

                          <template slot-scope="{row}">
                            <td><strong>{{ row.code }}</strong></td>
                            <td>{{ row.level.toFixed(2) }} µg/m³</td>
                            <td>{{ row.score }} %</td>
                          </template>

                        </base-table>
                      </div>


                      <!-- PLACES -->
                      <div v-if="detailsModal.provider != null && detailsModal.provider.id.startsWith('places-')" class="table-responsive">
                        <base-table class="table align-items-center table-flush"
                                    tbody-classes="list"
                                    :data="detailsModal.provider.data">
                          <template slot="columns">
                            <th>Place</th>
                            <th>Address</th>
                          </template>

                          <template slot-scope="{row}">
                            <td><strong>{{ row.title }}</strong></td>
                            <td>{{ row.address }}</td>
                          </template>

                        </base-table>
                      </div>
                   </div>
                   <template slot="footer">
                       <base-button type="secondary" @click="detailsModal.shown = false">Close</base-button>
                   </template>
                 </modal>

              </div>
            </div>
        </div>
    </div>
</template>
<script>
  export default {
    data() {
      return {
        detailsModal: {
          shown: false,
          provider: null,
        },
        place: null,/*{
          summary: {
            grade: 'okay',
            score: 55,
          },
          categories: [
            {
              title: 'Transport',
              icon: 'ni ni-bus-front-12',
              summary: {
                grade: 'good',
                score: 70,
              },
              providers: [
                {
                  id: 'parking',
                  summary: {
                    grade: "good",
                    score: 50,
                  },
                  data: [
                    {
                      title: 'Afternoon',
                      relative: 50,
                      absolute: 33,
                      capacity: 66,
                    }
                  ],
                  title: "Parking",
                },
              ],
            },
            {
              title: 'Health',
              icon: 'ni ni-favourite-28',
              summary: {
                grade: 'okay',
                score: 50,
              },
            },
            {
              title: 'Municipal',
              icon: 'ni ni-shop',
              summary: {
                grade: 'bad',
                score: 20,
              },
            },
          ],
        },*/
      };
    },
    methods: {
      displayDetails(row) {
        this.detailsModal.shown = true;
        this.detailsModal.provider = row;
      },

      callApi(endpoint, method, payload, callback, onError, payloadRaw) {
        var request = new XMLHttpRequest();

        request.onload = function () {
          // Request was successful
          if (this.status <= 299) {
            console.debug('Response received.', this.responseText);

            if (callback) {
              console.debug(`Parsing JSON...`);
              var data = this.responseText ? JSON.parse(this.responseText) : null;
              console.debug(`Calling callback...`);
              callback(data);
            }
          }

          // There was an issue with request
          else {
            console.debug('Request failed.', this.responseText);

            if (onError) {
              onError(this);
            } else {
              let responses = {
                404: 'Not found!',
                500: 'Server failure!',
              };

              let response = responses[this.status] || 'Unknown error!';
              //Swal.close();
              //Swal.fire(this.status.toString(), response, 'error');
              console.log(this.status.toString(), response);
            }
          }
        }

        var fullEndpoint = 'http://localhost:8000/' + endpoint;

        request.open(method, fullEndpoint);
        if (!payloadRaw) {
          request.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
          payload = JSON.stringify(payload);
        }
        request.send(payload);

        console.debug(`Sending '${method}' request to '${fullEndpoint}' with logged payload.`, payload);
      }
    },
    mounted() {
      var theme = 'http://{s}.tile.osm.org/{z}/{x}/{y}.png';
      var lat = 50.08804;
      var lon = 14.4207;
      var map = null;
      var marker = null;

      var component = this;

      function addMarker(latlng) {
        if (marker) {
          marker.remove();
        }
        marker = L.marker(latlng).addTo(map);

        component.place = null;
        component.callApi(`detect/${latlng.lat}/${latlng.lng}`, 'GET', null, data => {
          component.place = data;
        });
      }

      map = L.map('map-canvas').setView([lat, lon], 13);
      L.tileLayer(theme, {
        minZoom: 1,
        maxZoom: 20
      }).addTo(map);
      map.on('click', e => addMarker(e.latlng));
      addMarker({ lat: lat, lng: lon });
    }
  }
</script>
<style>
</style>
