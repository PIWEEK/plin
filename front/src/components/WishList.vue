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
            :serializer="item => item.name"
            @hit="selectedPlace = $event"
            placeholder="Escribe o busca el nombre del lugar, dirección o coordenadas"
            @input="searchPlaces"
            :showAllResults="true"
            :maxMatches="20"
            :disableSort="true"
          />
          <br/>
          <br/>
          <br/>
          <br/>
          <br/>
          <br/>
          <br/>
          <br/>
          <br/>
          <br/>
          <br/>
          <br/>
          <br/>
          <br/>
          <br/>
          <br/>
          <br/>
          <br/>
          <br/>
          <br/>
          <br/>
          <br/>
          <br/>
          <br/>
        </b-form-group>

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