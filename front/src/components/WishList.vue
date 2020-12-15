<template>
  <div class="wishlist">
    <b-button block variant="primary" v-b-modal.modal-new-plan>
      + Nuevo plan
    </b-button>
    <plan-card
      :name="plan.name"
      :image="plan.image"
      :id="plan.id"
      v-for="plan in $store.state.currentTrip.wishlist"
      :key="plan.id">
    </plan-card>

    <b-modal id="modal-new-plan" centered  size="xl" scrollable title="TODO: TITLE" cancel-disabled ok-disabled>
      <b-form @submit="onSubmit" @reset="onReset">
        <b-form-group
          id="input-group-1"
          label="Plan:"
          label-for="input-1"
        >

          <vue-type-ahead
            class="mb-4"
            v-model="query"
            :data="places"
            @hit="selectedPlace = $event"
            placeholder="Escribe o busca el nombre del lugar, dirección o coordenadas"
          />

        </b-form-group>

      </b-form>
    </b-modal>
  </div>
</template>

<script>
  import PlanCard from '@/components/PlanCard.vue'
  import VueBootstrapTypeahead from 'vue-bootstrap-typeahead'
  import axios from 'axios'

  export default {
    components: {
      'plan-card': PlanCard,
      'vue-type-ahead': VueBootstrapTypeahead
    },
    data() {
      return {
        query: '',
        selectedPlace: null,
        places: []
      }
    },
    watch: {
      // When the query value changes, fetch new results from
      // the API - TODO this action should be debounced
      query(newQuery) {
        console.log(newQuery)
        /*axios.get(`https://maps.googleapis.com/maps/api/place/textsearch/json?query=${newQuery}&key=AIzaSyAyRE60ZUO-zoDDZCDIMFwDgi7CRbIDDMo`)
          .then((res) => {
            console.log("RES", res)
            this.places = res.data.items
          })*/
      }
    },
    methods: {
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