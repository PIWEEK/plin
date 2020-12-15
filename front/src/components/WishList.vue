<template>
  <div class="wishlist">
    <b-button block variant="primary" v-b-modal.modal-new-plan>
      + Nuevo plan
    </b-button>
    <plan-card
      :plan="plan"
      v-for="plan in $store.state.currentTrip.wishlist"
      :key="plan.id">
    </plan-card>

    <b-modal id="modal-new-plan" centered  size="lg" scrollable title="Nuevo plan" hide-footer>
      <b-form @submit="onSubmit" @reset="onReset">
        <b-form-group
          id="input-group-plan"
          label="Plan"
          label-for="input-address"
        >
          <vue-type-ahead
            id="input-address"
            class="mb-4"
            v-model="query"
            :data="places"
            :serializer="item => item.name"
            @hit="selectedPlace = $event"
            placeholder="Escribe o busca el nombre del lugar, dirección o coordenadas"
            @input="searchPlaces"
            :showAllResults="true"
            :maxMatches="20"
            :disableSort="true"
          />
        </b-form-group>

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
          id="input-group-comments"
          label="Comentarios"
          label-for="input-comments"
        >
          <b-form-textarea
            id="input-address"
            v-model="address"
            rows="3"
            placeholder="¿Cuándo es mejor hacer este plan?, ¿hay que acordarse de llevar algo?, 
¡Cualquier cosa que te sirva para organizarte mejor! :)"/>
        </b-form-group>
      <b-button class="mt-3" block @click="$bvModal.hide('bv-modal-example')">Crear plan</b-button>

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
        query: '',
        selectedPlace: null,
        address: '',
        minPrice: null,
        maxPrice: null,
        duration: null,
        comments: null,
        places: []
      }
    },
    methods: {
      searchPlaces: _.debounce(function(){
        // in practice this action should be debounced
        fetch(`https://cors-anywhere.herokuapp.com/https://maps.googleapis.com/maps/api/place/textsearch/json?query=${this.query}&key=AIzaSyAyRE60ZUO-zoDDZCDIMFwDgi7CRbIDDMo`)
          .then(response => {
            return response.json();
          })
          .then(data => {
            this.places = data.results
          })
      }, 500),
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