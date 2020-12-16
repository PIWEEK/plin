<template>
  <div class="wishlist">
    <b-button block variant="primary" @click="showModal()">
      + Nuevo plan
    </b-button>
    <div 
      style="width: 100%; height: 100%"
      class="drop-zone"
      @drop='onDrop($event, 1)' 
      @dragover.prevent
      @dragenter.prevent
      >
        <plan-card
          :plan="plan"
          v-for="plan in $store.state.currentTrip.wishlist"
          v-on:plan_drop_on_child="planDropOnChild"
          :key="plan.id">
        </plan-card>
    </div>

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
        console.log("this.$store.state.currentUser", this.$store.state.currentUser.token);

        fetch(`http://localhost:8000/api/trips/search?place=${this.place}`, {
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
        this.place = place.name;
        this.address = place.formatted_address;
        this.telephone = place.telephone;

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
            this.address = data.result.formatted_address;
            this.telephone = data.result.international_phone_number;
            this.openingHours = data.result.opening_hours.weekday_text.join("\n");
          })

      },
      onSubmit: () => {

      },
      onReset: () => {
      },
      async movePlan(planId){
          this.$store.commit("SET_SHOWSPINNER", true);
          await this.$store.dispatch("movePlan", {"planId": planId, "dayId": null});
          await this.$store.dispatch("fetchTrip");
          this.$store.commit("SET_SHOWSPINNER", false);
      },
      async createPlan() {                
        this.$store.commit("SET_SHOWSPINNER", true);
        const newPlan = {
                  "name": this.place,
                  "url_picture": "https://picsum.photos/200",
                  "price_min": this.minPrice,
                  "price_max": this.maxPrice,
                  "duration": this.duration ? this.duration : 1,
                  "address": this.address,
                  "telephone": this.telephone,
                  "opening_hours": this.openingHours,
                  "comments": this.comments,
                  "order": 1,
                  "trip": this.$store.state.currentTrip.id
                  }


        await this.$store.dispatch("createPlan", newPlan);
        await this.$store.dispatch("fetchTrip");
        this.$bvModal.hide('modal-new-plan');
        this.$store.commit("SET_SHOWSPINNER", false);
      },
      onDrop (evt) {
        const planId = evt.dataTransfer.getData('planId');
        console.log("onDrop "+planId);
        this.movePlan(planId);
      },
      planDropOnChild (planId, position) {          
        console.log("planDropOnChild: " + planId+ " - position: "+position);
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