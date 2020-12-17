<template>
  <b-container>
    <b-container class="create-trip">
      <h1 class="title">¡Haz las maletas!</h1>
      <b-container class="create-trip-form">
        <b-form>
          <b-form-group
            id="input-group-travel"
            label="Viaje"
            label-for="input-travel"
          >
            <vue-type-ahead
              id="input-travel"
              class="mb-4"
              v-model="place"
              :data="places"
              :serializer="item => item.name"
              @hit="onSelectedPlace($event)"
              placeholder="¡Ponle un título a tu viaje!"
              @input="searchPlaces"
              :showAllResults="true"
              :maxMatches="20"
              :disableSort="true"
            />

          </b-form-group>

          <b-form-group
            id="input-group-address"
            label="Fechas"
            label-for="input-date"
          >
            <b-row>
              <b-col>
                <b-form-datepicker
                  :date-format-options="{ year: '2-digit', month: '2-digit', day: '2-digit', weekday: 'narrow' }"
                  locale="es"
                  placeholder="Fecha inicial"
                  id="initial-date"
                  v-model="initialDate"
                  class="mb-2"
                  :disabled="noDates"/>
              </b-col>
              <b-col>
                <b-form-datepicker
                  :date-format-options="{ year: '2-digit', month: '2-digit', day: '2-digit', weekday: 'narrow' }"
                  locale="es"
                  placeholder="Fecha de fin"
                  id="end-date"
                  v-model="endDate"
                  class="mb-2"
                  :disabled="noDates"/>
                </b-col>
              <b-col class="my-auto">
                <b-form-checkbox
                  id="checkbox-no-dates"
                  v-model="noDates"
                  name="checkbox-no-dates"
                >
                  Aún no sé fechas
                </b-form-checkbox>
              </b-col>
            </b-row>
          </b-form-group>
          <b-button variant="primary" class="create-button" :disabled="!validForm" block @click="createTrip()">Comenzar</b-button>
        </b-form>
      </b-container>
    </b-container>

    <h1 v-if="$store.state.trips.length > 0" style="margin-top: 5rem">Próximos Viajes</h1>
    <trips v-if="$store.state.trips.length > 0"/>
    <h1 v-if="$store.state.trips.length > 0" style="margin-top: 5rem">Viajes pasados</h1>
    <trips v-if="$store.state.trips.length > 0" />
  </b-container>
</template>

<script>
import Trips from '@/components/Trips.vue';
import VueTypeaheadBootstrap from 'vue-typeahead-bootstrap';
import {_} from 'vue-underscore';

export default {
  name: "Home",
  components: {
    'trips': Trips,
    'vue-type-ahead': VueTypeaheadBootstrap
  },
  data() {
    return {
      place: null,
      initialDate: null,
      endDate: null,
      noDates: false,
      urlPicture: `${window.location.origin}/images/default-trip-${1 + Math.floor(Math.random() * Math.floor(9))}.png`,
      duration: null,
      places: []
    }
  },
  computed: {
    validForm: function() {
      if (!this.place) {
        return false
      }
      if (this.noDates) {
        return true;
      }
      return this.initialDate && this.endDate;
    }
  },
  async mounted() {
    if (this.$store.state.currentUser.token === undefined){
      this.$router.push("/");
    } else if (this.$store.state.currentUser.name === undefined){
      this.getUserInfo();
    }
  },
  methods: {
    searchPlaces: _.debounce(function(){
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
          var maxRatio = 0;
          var bestPhoto = null;
          if (data.result.photos) {
            data.result.photos.forEach(photo => {
              const ratio = photo.width / photo.height;
              if (ratio > maxRatio) {
                maxRatio = ratio,
                bestPhoto = photo;
              }
            });

            fetch(`http://localhost:8000/api/trips/photo?maxwidth=1600&photoreference=${bestPhoto.photo_reference}`, {
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
                this.urlPicture = photoData.url;
              });
          }
        })
    },
    createTrip: async function() {
      this.duration = 3;
      if (this.initialDate && this.endDate) {
        const dt1 = new Date(this.initialDate);
        const dt2 = new Date(this.endDate);
        this.duration = Math.floor((Date.UTC(dt2.getFullYear(), dt2.getMonth(), dt2.getDate()) - Date.UTC(dt1.getFullYear(), dt1.getMonth(), dt1.getDate()) ) /(1000 * 60 * 60 * 24));
      }

      const trip = {
        "duration": this.duration,
        "from_date": this.initialDate,
        "title": this.place,
        "to_date": this.endDate,
        "url_picture": this.urlPicture
      }

      this.$store.commit("SET_SHOWSPINNER", true);

      await this.$store.dispatch("createTrip", trip);
      await this.$store.dispatch("fetchTripsList");
      this.$store.commit("SET_SHOWSPINNER", false);
    },
    async getUserInfo() {
      const userInfo = await this.$store.dispatch("me", JSON.stringify(this.form));
      var currentUser = this.$store.state.currentUser;
      currentUser["name"] = userInfo.first_name;
      currentUser["id"] = userInfo.id;
      this.$store.commit("SET_CURRENTUSER", currentUser);
    }
  }
};
</script>

<style lang="scss">
  .title {
    color: #150101;
    font-size: 86px;
    font-weight: bold;
  }

  .create-trip {
     background-image: url("/create_trip_bg.png");
     background-size: cover;
     padding: 30px 85px 60px 85px;
  }

  .create-trip-form {
    background-color: rgba(255, 255, 255, 0.8);
    border-radius: 30px;
    max-width: 630px;
    margin: 20px 30px;
    padding: 28px 52px ;
  }

  .create-button {
    margin-top: 40px;
  }
</style>
