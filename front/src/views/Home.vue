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
            <b-form-input
            id="input-travel"
            v-model="title"
            placeholder="¡Ponle un título a tu viaje!"/>
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
          <b-button variant="primary" :disabled="!validForm" block @click="createTrip()">Comenzar</b-button>
        </b-form>
      </b-container>
    </b-container>

    <h1 style="margin-top: 5rem">Próximos Viajes</h1>
    <trips />
    <h1 style="margin-top: 5rem">Viajes pasados</h1>
    <trips />
  </b-container>
</template>

<script>
import Trips from '@/components/Trips.vue'

export default {
  name: "Home",
  components: {
    'trips': Trips
  },
  data() {
    return {
      title: null,
      initialDate: null,
      endDate: null,
      noDates: false
    }
  },
  computed: {
    validForm: function() {
      if (!this.title) {
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
    }
  },
  methods: {
    createTrip: async function() {
      console.log("TODO: create trip");

      var duration = 4;
      if (this.initialDate && this.endDate) {
        const dt1 = new Date(this.initialDate);
        const dt2 = new Date(this.endDate);
        duration = Math.floor((Date.UTC(dt2.getFullYear(), dt2.getMonth(), dt2.getDate()) - Date.UTC(dt1.getFullYear(), dt1.getMonth(), dt1.getDate()) ) /(1000 * 60 * 60 * 24));
      }

      const trip = {
        "duration": duration,
        "from_date": this.initialDate,
        "title": this.title,
        "to_date": this.endDate
      }

      this.$store.commit("SET_SHOWSPINNER", true);
      await this.$store.dispatch("createTrip", trip);
      await this.$store.dispatch("fetchTripsList");
      this.$store.commit("SET_SHOWSPINNER", false);
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
    margin: 0;
    padding: 28px 52px ;
  }
</style>
