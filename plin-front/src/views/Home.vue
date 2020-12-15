<template>
<b-container>
  <b-row>
  My trips:
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

  }
};
</script>
