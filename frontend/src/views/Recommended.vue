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
                <div class="col-6">
                    <card shadow>
                      <h1>Recommended places</h1>

                      <div class="card shadow">
                        <div class="table-responsive">
                          <base-table class="table align-items-center table-flush"
                                      tbody-classes="list"
                                      :data="places">
                            <template slot="columns">
                              <th>Name</th>
                              <th>Score</th>
                              <th>Show</th>
                            </template>

                            <template slot-scope="{row}">
                              <td :class="{ activeRow: (row.id == activeId) }">{{ row.title }}</td>
                              <td :class="{ activeRow: (row.id == activeId) }">{{ row.score.toFixed(2) }} %</td>
                              <td :class="{ activeRow: (row.id == activeId) }">
                                <base-button type="primary" size="sm" @click="showOnMap(row)">
                                  Show
                                </base-button>
                              </td>
                            </template>

                          </base-table>
                        </div>
                      </div>
                    </card>
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
        map: null,
        marker: null,
        activeId: 0,
        places: [
          {
            id: 1,
            title: 'Smíchov',
            lat: 50.07179454832413,
            lon: 14.400064909133365,
            score: 86.11,
          },
          {
            id: 2,
            title: 'Josefov',
            lat: 50.09019056811813,
            lon: 14.419163406556825,
            score: 81.94,
          },
          {
            id: 3,
            title: 'Hlavní nádraží',
            lat: 50.082480520955926,
            lon: 14.430676324576835,
            score: 78.89,
          },
          {
            id: 4,
            title: 'Hradčany',
            lat: 50.08617048398654,
            lon: 14.39760626264584,
            score: 78.06,
          },
          {
            id: 5,
            title: 'Žižkov',
            lat: 50.08118621290215,
            lon: 14.44571128887559,
            score: 76.11,
          },
        ],
      };
    },
    methods: {
      showOnMap(row) {
        if (this.marker) {
          this.marker.remove();
        }
        this.marker = L.marker({ lat: row.lat, lng: row.lon }).addTo(this.map);
        this.map.setView([row.lat, row.lon], 13);
        this.activeId = row.id;
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

      this.map = L.map('map-canvas').setView([lat, lon], 13);
      L.tileLayer(theme, {
        minZoom: 1,
        maxZoom: 20
      }).addTo(this.map);
      this.showOnMap(this.places[0]);
    }
  }
</script>
<style>
</style>
