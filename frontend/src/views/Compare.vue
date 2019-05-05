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
                <div v-if="place1 != null && place2 != null" class="col-6">
                  <tabs fill class="flex-column flex-md-row">
                    <card shadow>
                        <tab-pane>
                            <span slot="title">
                                <i class="ni ni-satisfied"></i>
                                Summary
                            </span>
                            <div class="description">
                              <h1>Summary:
                                <span style="color: blue">
                                  <badge v-if="place1.summary.grade == 'good'" type="success">Good</badge>
                                  <badge v-if="place1.summary.grade == 'okay'" type="warning">Okay</badge>
                                  <badge v-if="place1.summary.grade == 'bad'" type="danger">Bad</badge>
                                  <span class="small">&nbsp;({{ place1.summary.score.toFixed(2) }} %)</span>
                                </span>
                                &nbsp; vs. &nbsp;
                                <span style="color: violet">
                                  <badge v-if="place2.summary.grade == 'good'" type="success">Good</badge>
                                  <badge v-if="place2.summary.grade == 'okay'" type="warning">Okay</badge>
                                  <badge v-if="place2.summary.grade == 'bad'" type="danger">Bad</badge>
                                  <span class="small">&nbsp;({{ place2.summary.score.toFixed(2) }} %)</span>
                                </span>
                              </h1>

                              <div class="card shadow">
                                <div class="table-responsive">
                                  <base-table class="table align-items-center table-flush"
                                              tbody-classes="list"
                                              :data="iterable(place1.categories)">
                                    <template slot="columns">
                                      <th>Category</th>
                                      <th style="color: blue">Place 1</th>
                                      <th style="color: violet">Place 2</th>
                                    </template>

                                    <template slot-scope="{index}">
                                      <td>
                                        <i :class="place1.categories[index].icon"></i>
                                        {{ place1.categories[index].title }}
                                      </td>
                                      <td style="color: blue">
                                        {{ place1.categories[index].summary.score.toFixed(2) }} %
                                        <badge v-if="place1.categories[index].summary.grade == 'good'" type="success">Good</badge>
                                        <badge v-if="place1.categories[index].summary.grade == 'okay'" type="warning">Okay</badge>
                                        <badge v-if="place1.categories[index].summary.grade == 'bad'" type="danger">Bad</badge>
                                      </td>
                                      <td style="color: violet">
                                        {{ place2.categories[index].summary.score.toFixed(2) }} %
                                        <badge v-if="place2.categories[index].summary.grade == 'good'" type="success">Good</badge>
                                        <badge v-if="place2.categories[index].summary.grade == 'okay'" type="warning">Okay</badge>
                                        <badge v-if="place2.categories[index].summary.grade == 'bad'" type="danger">Bad</badge>
                                      </td>
                                    </template>

                                  </base-table>
                                </div>
                              </div>

                            </div>
                        </tab-pane>

                        <tab-pane v-for="index in iterable(place1.categories)" :title="place1.categories[index].title">
                            <span slot="title">
                                <i :class="place1.categories[index].icon"></i>
                                {{ place1.categories[index].title }}
                            </span>
                            <div class="description">
                              <h1>{{ place1.categories[index].title }}:
                                <span style="color: blue">
                                  <badge v-if="place1.categories[index].summary.grade == 'good'" type="success">Good</badge>
                                  <badge v-if="place1.categories[index].summary.grade == 'okay'" type="warning">Okay</badge>
                                  <badge v-if="place1.categories[index].summary.grade == 'bad'" type="danger">Bad</badge>
                                  <span class="small">&nbsp;({{ place1.categories[index].summary.score.toFixed(2) }} %)</span>
                                </span>
                                &nbsp; vs. &nbsp;
                                <span style="color: violet">
                                  <badge v-if="place2.categories[index].summary.grade == 'good'" type="success">Good</badge>
                                  <badge v-if="place2.categories[index].summary.grade == 'okay'" type="warning">Okay</badge>
                                  <badge v-if="place2.categories[index].summary.grade == 'bad'" type="danger">Bad</badge>
                                  <span class="small">&nbsp;({{ place2.categories[index].summary.score.toFixed(2) }} %)</span>
                                </span>
                              </h1>

                              <div class="card shadow">
                                <div class="table-responsive">
                                  <base-table class="table align-items-center table-flush"
                                              tbody-classes="list"
                                              :data="iterable(place1.categories[index].providers)">
                                    <template slot="columns">
                                      <th>Provider</th>
                                      <th>Grade 1</th>
                                      <th>Grade 2</th>
                                    </template>

                                    <template slot-scope="{row}">
                                      <td>
                                        {{ place1.categories[index].providers[row].title }}
                                      </td>
                                      <td style="color: blue">
                                        {{ place1.categories[index].providers[row].summary.score.toFixed(2) }} %
                                        <badge v-if="place1.categories[index].providers[row].summary.grade == 'good'" type="success">Good</badge>
                                        <badge v-if="place1.categories[index].providers[row].summary.grade == 'okay'" type="warning">Okay</badge>
                                        <badge v-if="place1.categories[index].providers[row].summary.grade == 'bad'" type="danger">Bad</badge>
                                      </td>
                                      <td style="color: violet">
                                        {{ place2.categories[index].providers[row].summary.score.toFixed(2) }} %
                                        <badge v-if="place2.categories[index].providers[row].summary.grade == 'good'" type="success">Good</badge>
                                        <badge v-if="place2.categories[index].providers[row].summary.grade == 'okay'" type="warning">Okay</badge>
                                        <badge v-if="place2.categories[index].providers[row].summary.grade == 'bad'" type="danger">Bad</badge>
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
                  <i v-if="place1 != null || place2 != null" class="fas fa-spinner fa-pulse"></i>
                </div>
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
        place1: null,
        place2: null,/*{
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
      },

      iterable(arr) {
        var len = arr.length;
        var nums = [];
        for (var i = 0; i < len; i++) {
          nums.push(i);
        }
        return nums;
      }
    },
    mounted() {
      var theme = 'http://{s}.tile.osm.org/{z}/{x}/{y}.png';
      var lat = 50.08804;
      var lon = 14.4207;
      var map = null;
      var firstMarker = null;
      var secondMarker = null;
      var activeFirst = true;

      var firstStyle = new L.Icon({
        iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
      });

      var secondStyle = new L.Icon({
        iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-violet.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
      });

      var component = this;

      function addMarker(latlng) {
        var old = activeFirst ? firstMarker : secondMarker;
        if (old) {
          old.remove();
        }
        var icon = activeFirst ? firstStyle : secondStyle;
        var marker = L.marker(latlng, { icon: icon }).addTo(map);
        if (activeFirst) {
          firstMarker = marker;
          component.place1 = null;
        } else {
          secondMarker = marker;
          component.place2 = null;
        }
        activeFirst = !activeFirst;

        var activeTemp = !activeFirst;
        component.place = null;
        component.callApi(`detect/${latlng.lat}/${latlng.lng}`, 'GET', null, data => {
          if (activeTemp) {
            component.place1 = data;
          } else {
            component.place2 = data;
          }
        });
      }

      map = L.map('map-canvas').setView([lat, lon], 13);
      L.tileLayer(theme, {
        minZoom: 1,
        maxZoom: 20
      }).addTo(map);
      map.on('click', e => addMarker(e.latlng));
    }
  }
</script>
<style>
</style>
