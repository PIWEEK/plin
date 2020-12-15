<template>
<b-container>
  <b-row>
    {{this.$store.state.currentTrip.name}}
  </b-row>

  <b-row class="text-center">
    <b-col style="border: 1px solid green">
      <wishlist></wishlist>
    </b-col>
    <b-col style="border: 1px solid green" cols="10">
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
  }
};
</script>
