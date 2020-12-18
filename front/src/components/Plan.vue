<template>
    <b-modal id="modal-new-plan" centered  size="lg" scrollable :title="getTitle" style="height: 50rem">
      <b-form style="width: 90%; margin-left: 5%">

        <b-form-group
            id="input-group-plan"
            label="Plan"
            label-for="input-address"
          >
            <vue-type-ahead
              id="input-name"
              class="mb-4"
              v-model="plan.name"
              :data="places"
              :serializer="item => item.name"
              @hit="onSelectedPlace($event)"
              placeholder="Escribe o busca el nombre del lugar, dirección o coordenadas"
              @input="searchPlaces"
              :showAllResults="true"
              :maxMatches="20"
              :disableSort="true"
            />
          </b-form-group>

        <b-container >
          <b-row style="height: 12rem">
            <b-col cols="4" v-if="plan.id != null" style="position:relative">
              <b-img :src="plan.url_picture" style="height: 11rem; width: 11rem"></b-img>
              <div style="position:absolute; top:0.2rem; right: 2.2rem; cursor:pointer" v-on:click="$bvToast.show('img-toast')">
                <b-img width="44px" style="padding: 8px" src="/edit.png"></b-img>
              </div>
              <b-toast id="img-toast" title="Cambiar imagen" static no-auto-hide style="width: 40rem; position: absolute; top:0; left:0">
                <b-form-input
                  id="input-address"
                  v-model="plan.url_picture"
                  placeholder="Copia la URL de la imagen aquí "/>
              </b-toast>

            </b-col>
            <b-col :style="plan.id  ? 'padding-left: 15px' : 'padding-left: 0'">
              <b-form-group
                id="input-group-address"
                label="Dirección"
                label-for="input-address"
              >
                <b-form-input
                  id="input-address"
                  v-model="plan.address"
                  placeholder="Escribe la dirección"/>
              </b-form-group>

              <b-form-group
                id="input-group-telephone"
                label="Teléfono"
                label-for="input-telephone"
              >
                <b-form-input
                  id="input-telephone"
                  v-model="plan.telephone"
                  placeholder="Escribe el teléfono"/>
              </b-form-group>
            </b-col>
          </b-row>
        </b-container>



        <b-row>
          <b-col>
            <b-form-group
              id="input-group-address"
              label="Precio"
              label-for="input-price"
            >
              <b-row>
                <b-col>
                  <b-form-input
                    id="input-min-price"
                    v-model="plan.price_min"
                    placeholder="Mínimo"/>
                </b-col>
                <b-col>
                  <b-form-input
                    id="input-max-price"
                    v-model="plan.price_max"
                    placeholder="Máximo"/>
                  </b-col>
              </b-row>
            </b-form-group>
          </b-col>

          <b-col>
            <b-form-group
              id="input-group-duration"
              label="Duración (en horas)"
              label-for="input-duration"
            >
              <b-form-input
                id="input-duration"
                v-model="plan.duration"
                placeholder="¿Cuánto durará el plan?"/>
            </b-form-group>
          </b-col>
        </b-row>
        <b-row>
          <b-col>
            <b-form-group
              id="input-group-opening-hours"
              label="Horario"
              label-for="input-opening-hours"
            >
              <b-form-textarea
                id="input-address"
                v-model="plan.opening_hours"
                rows="3"
                placeholder="Escribe los horarios de apertura"/>
            </b-form-group>
          </b-col>
          <b-col>
            <b-form-group label="Tipo">
              <b-form-radio-group
                id="radio-group-type"
                v-model="plan.plan_type"
              >
                <b-container>
                  <b-row>
                    <b-col>
                      <b-form-radio value="Culture">Cultura</b-form-radio>
                      <b-form-radio value="Gastronomy">Gastronomía</b-form-radio>
                      <b-form-radio value="Walk">Naturaleza</b-form-radio>
                    </b-col>
                    <b-col>
                      <b-form-radio value="Walk">Paseo</b-form-radio>
                      <b-form-radio value="Other">Otro</b-form-radio>
                    </b-col>
                  </b-row>
                </b-container>


              </b-form-radio-group>
            </b-form-group>
          </b-col>
        </b-row>

        <b-form-group
          id="input-group-comments"
          label="Comentarios"
          label-for="input-comments"
        >
          <b-form-textarea
            id="input-address"
            v-model="plan.comments"
            rows="3"
            placeholder="¿Cuándo es mejor hacer este plan?, ¿hay que acordarse de llevar algo?,
¡Cualquier cosa que te sirva para organizarte mejor! :)"/>
        </b-form-group>
      </b-form>


      <template #modal-footer="{ cancel}">
        <!-- Emulate built in modal footer ok and cancel button actions -->
        <b-button size="sm" variant="outline-secondary" @click="cancel()">
          Cerrar
        </b-button>
        <b-button size="sm" @click="createOrUpdatePlan()">
          Guardar cambios
        </b-button>
      </template>



    </b-modal>
</template>

<script>
  import VueTypeaheadBootstrap from 'vue-typeahead-bootstrap';
  import {_} from 'vue-underscore';

  export default {
    components: {
      'vue-type-ahead': VueTypeaheadBootstrap
    },
    data() {
      return {
        plan: {
          url_picture: `${window.location.origin}/images/default-plan-${1 + Math.floor(Math.random() * Math.floor(6))}.png`
        },
        title: '',
        places: []
      }
    },
    computed: {
      getTitle(){
        return this.plan.id == null ? 'Alta de plan' : 'Detalles de Plan';
      }
    },
    methods: {
      searchPlaces: _.debounce(function(){
        fetch(`http://localhost:8000/api/trips/search?place=${this.plan.name}`, {
            headers: {
              'Authorization': 'JWT '+ this.$store.state.currentUser.token,
              'Accept': 'application/json',
              'Content-Type': 'application/json'
            }
          })
          .then(response => {
            return response.json();
          })
          .then(data => {
            this.places = data.results
          })
      }, 500),
      onSelectedPlace: function(place) {
        this.selectedPlace = place;
        this.plan.name = place.name;
        this.plan.address = place.formatted_address;
        this.plan.telephone = place.telephone;

        fetch(`http://localhost:8000/api/trips/locate?place_id=${place.place_id}`, {
            headers: {
              'Authorization': 'JWT '+ this.$store.state.currentUser.token,
              'Accept': 'application/json',
              'Content-Type': 'application/json'
            }
          })
          .then(response => {
            return response.json();
          })
          .then(data => {
            var bestRatio = null;
            var bestPhoto = null;
            if (data.result.photos) {
              data.result.photos.forEach(photo => {
                const ratio = (photo.width / photo.height) - 1;
                if (!bestRatio || (ratio > 0 && ratio < bestRatio)) {
                  bestRatio = ratio,
                  bestPhoto = photo;
                }
              });

              fetch(`http://localhost:8000/api/trips/photo?maxwidth=500&photoreference=${bestPhoto.photo_reference}`, {
                  headers: {
                    'Authorization': 'JWT '+ this.$store.state.currentUser.token,
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                  }
                })
                .then(photoResponse => {
                  return photoResponse.json();
                })
                .then(photoData => {
                  this.plan.url_picture = photoData.url;
                });
            }
            else {
              this.plan.url_picture = `${window.location.origin}/images/default-plan-${1 + Math.floor(Math.random() * Math.floor(6))}.png`;
            }
            this.plan.address = data.result.formatted_address;
            this.plan.telephone = data.result.international_phone_number;
            if (data.result.opening_hours) {
              this.plan.opening_hours = data.result.opening_hours.weekday_text.join("\n");
            }

            if (data.result.geometry) {
              this.plan.latlon = {
                type: "Point",
                coordinates: [
                  data.result.geometry.location.lat,
                  data.result.geometry.location.lng
                ]
              }
            }
          })
      },
      onSubmit: () => {

      },
      onReset: () => {
      },
      async createOrUpdatePlan() {
        this.$store.commit("SET_SHOWSPINNER", true);
        await this.$store.dispatch(this.plan.id === null ? "createPlan" : "updatePlan", this.plan);
        await this.$store.dispatch("fetchTrip");
        this.$bvModal.hide('modal-new-plan');
        this.$store.commit("SET_SHOWSPINNER", false);
      },
      fillPlan(plan){
        this.places = [];
        if (plan == null) {
          plan = {
            "id": null,
            "address": null,
            "comments": null,
            "duration": 1,
            "google_id": null,
            "latlon": null,
            "name": null,
            "opening_hours": null,
            "plan_type": "Other",
            "popular_times": null,
            "price_max": null,
            "price_min": null,
            "telephone": null,
            "url_picture": `${window.location.origin}/images/default-plan-${1 + Math.floor(Math.random() * Math.floor(6))}.png`,
            "day": null,
            "trip": this.$store.state.currentTrip.id
          }
        } else {
          delete plan['created_by'];
          delete plan['distance_to_next'];
          delete plan['order'];
          delete plan['created_at'];
        }

        this.plan = plan;
      },
      async duplicatePlan(plan){
        this.fillPlan(plan);
        this.plan.id=null;
        this.plan.name="Copia de "+this.plan.name;
        await this.createOrUpdatePlan();
      }
    }
  }
</script>

<style lang="scss" scoped>
  .btn-primary {
    color: #fff;
    background-color: #97d6e0;
    border-color: #97d6e0;
  }

  .btn-primary:hover {
    color: #fff;
    background-color: #53cde0;
    border-color: #53cde0;
  }
</style>

