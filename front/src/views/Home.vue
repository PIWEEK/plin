<template>
  <b-container>
    <b-row>
      <h1 style="margin-top: 5rem">Próximos Viajes</h1>
    </b-row>
    <trips />
    <b-row>
      <h1 style="margin-top: 5rem">Viajes pasados</h1>
    </b-row>
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
  async mounted() {
    if (this.$store.state.currentUser.token === undefined){
      this.$router.push("/");
    }
  },
};
</script>
