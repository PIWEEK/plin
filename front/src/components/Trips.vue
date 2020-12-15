<template>
    <b-container>
      <b-row align-v="center">
        <trip-card
          :name="trip.name"
          :image="trip.image"
          :start="trip.start"
          :end="trip.end"
          :duration="trip.duration"
          :id="trip.id"
          v-for="trip in getTrips"
          :key="trip.id"
        ></trip-card>
      </b-row>
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
        await this.$store.dispatch("fetchTripsList");
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