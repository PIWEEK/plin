<template>
  <div class="wishlist">
    <b-button block variant="primary" @click="showModal()">
      + Nuevo plan
    </b-button>
    <plan-card
      :plan="plan"
      v-for="plan in $store.state.currentTrip.wishlist"
      :key="plan.id">
    </plan-card>

    <b-modal id="modal-new-plan" centered  size="lg" scrollable title="Nuevo plan" hide-footer>
      <b-form>
        <b-form-group
          id="input-group-plan"
          label="Plan"
          label-for="input-address"
        >
          <vue-type-ahead
            id="input-address"
            class="mb-4"
            v-model="place"
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

        <b-row>
          <b-col>
            <b-form-group
              id="input-group-address"
              label="Dirección"
              label-for="input-address"
            >
              <b-form-input
                id="input-address"
                v-model="address"
                placeholder="Escribe la dirección"/>
            </b-form-group>
          </b-col>

          <b-col>
            <b-form-group
              id="input-group-telephone"
              label="Teléfono"
              label-for="input-telephone"
            >
              <b-form-input
                id="input-telephone"
                v-model="telephone"
                placeholder="Escribe el teléfono"/>
            </b-form-group>
          </b-col>
        </b-row>
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
                    v-model="minPrice"
                    placeholder="Mínimo"/>
                </b-col>
                <b-col>
                  <b-form-input
                    id="input-max-price"
                    v-model="maxPrice"
                    placeholder="Máximo"/>
                  </b-col>
              </b-row>
            </b-form-group>
          </b-col>

          <b-col>
            <b-form-group
              id="input-group-duration"
              label="Duración"
              label-for="input-duration"
            >
              <b-form-input
                id="input-duration"
                v-model="duration"
                placeholder="¿Cuánto durará el plan?"/>
            </b-form-group>
          </b-col>
        </b-row>

        <b-form-group
          id="input-group-opening-hours"
          label="Horarios"
          label-for="input-opening-hours"
        >
          <b-form-textarea
            id="input-address"
            v-model="openingHours"
            rows="3"
            placeholder="Escribe los horarios en los que se puede visitar"/>
        </b-form-group>

        <b-form-group
          id="input-group-comments"
          label="Comentarios"
          label-for="input-comments"
        >
          <b-form-textarea
            id="input-address"
            v-model="comments"
            rows="3"
            placeholder="¿Cuándo es mejor hacer este plan?, ¿hay que acordarse de llevar algo?, 
¡Cualquier cosa que te sirva para organizarte mejor! :)"/>
        </b-form-group>
        <b-button variant="primary" block @click="createPlan()">Crear plan</b-button>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
  import PlanCard from '@/components/PlanCard.vue';
  import VueTypeaheadBootstrap from 'vue-typeahead-bootstrap';
  import {_} from 'vue-underscore';

  export default {
    components: {
      'plan-card': PlanCard,
      'vue-type-ahead': VueTypeaheadBootstrap
    },
    data() {
      return {
        selectedPlace: null,
        place: null,
        address: null,
        telephone: null,
        openingHours: null,
        minPrice: null,
        maxPrice: null,
        duration: null,
        comments: null,
        places: []
      }
    },
    methods: {
      showModal: function() {
        this.selectedPlace = null;
        this.place = null;
        this.address = null;
        this.telephone = null;
        this.openingHours = null;
        this.minPrice = null;
        this.maxPrice = null;
        this.duration = null;
        this.comments = null;
        this.places = [];
        this.$bvModal.show('modal-new-plan');
      },
      searchPlaces: _.debounce(function(){
        fetch(`https://cors-anywhere.herokuapp.com/https://maps.googleapis.com/maps/api/place/textsearch/json?query=${this.place}&key=${process.env.VUE_APP_GOOGLE_API_KEY}`)
          .then(response => {
            return response.json();
          })
          .then(data => {
            this.places = data.results
          })
      }, 500),
      onSelectedPlace: function(place) {
        this.selectedPlace = place;
        this.place = place.name;
        this.address = place.formatted_address;
        this.telephone = place.telephone;

        fetch(`https://cors-anywhere.herokuapp.com/https://maps.googleapis.com/maps/api/place/details/json?place_id=${place.place_id}&key=${process.env.VUE_APP_GOOGLE_API_KEY}`)
          .then(response => {
            return response.json();
          })
          .then(data => {
            this.address = data.result.formatted_address;
            this.telephone = data.result.international_phone_number;
            this.openingHours = data.result.opening_hours.weekday_text.join("\n");
          })

      },
      createPlan: function() {
        console.log('TODO: create plan');
        this.$bvModal.hide('modal-new-plan');
      },
      onSubmit: () => {

      },
      onReset: () => {
      }
    }
  }
</script>

<style lang="scss" scoped>
  .wishlist {
    background-color: lightblue;
    border: 1px solid black;
    height: 300px;
    width: 100%;
  }
</style>