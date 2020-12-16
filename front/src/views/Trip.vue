<template>
  <b-container>
    <div class="d-flex align-items-center header" :style="headerImg">
        <div class="w-100"><h1>{{this.$store.state.currentTrip.name}}</h1></div>
    </div>

    <b-row class="text-center">
      <b-col cols="3">
        <wishlist></wishlist>
      </b-col>
      <b-col cols="9">
      <week></week>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import WishList from '@/components/WishList.vue'
import Week from '@/components/Week.vue'

export default {
  name: "Trip",
  async mounted() {
    this.getRecords();
  },
  components: {
    'wishlist': WishList,
    'week': Week
  },
  data() {
    return {
    };
  },
  methods: {
    async getRecords() {
      await this.$store.dispatch("fetchTrip");
    }
  },
  computed: {
      headerImg () {
        return "background-image: url('" + this.$store.state.currentTrip.image + "')";
      }
    },
};
</script>

<style lang="scss" scoped>

.header {
  color: white;  
  background-color: #cccccc; /* Used if the image is unavailable */
  height: 8rem; /* You must set a specified height */
  background-position: center; /* Center the image */
  background-repeat: no-repeat; /* Do not repeat the image */
  background-size: cover; /* Resize the background image to cover the entire container */
}

</style>