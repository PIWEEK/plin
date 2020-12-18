<template>
  <b-container fluid p-0>
    <b-row align-v="center">
      <trip-card
        :title="trip.title"
        :url_picture="trip.url_picture"
        :start="trip.from_date"
        :end="trip.to_date"
        :duration="trip.duration"
        :id="trip.id"
        v-for="trip in getTrips"
        :key="trip.id"
      ></trip-card>
    </b-row>
    <div v-if="getTrips.length == 0" style="margin-top:2rem">
      <h4>Todavía no tienes ningún viaje :(</h4>
    </div>
  </b-container>
</template>

<script>
// @ is an alias to /src
import TripCard from "@/components/TripCard.vue";
import { mapGetters } from "vuex";
export default {
  name: "trips",
  async mounted() {
    this.getRecords();
  },
  data() {
    return {

    };
  },
  components: { "trip-card": TripCard },
  computed: {
    ...mapGetters(["getTrips"])
  },
  methods: {
    async getRecords() {
      if (this.$store.state.currentUser.token !== undefined){
        this.$store.commit("SET_SHOWSPINNER", true);
        await this.$store.dispatch("fetchTripsList");
        this.$store.commit("SET_SHOWSPINNER", false);
      }
    }
  }
};
</script>
<style lang="scss" scoped>
// b-card {
// padding: 10px;
// }
</style>