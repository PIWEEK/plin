<template>
<b-container style="width: 100%; text-align: left; overflow-x: hidden">
  <b-row class="flex-nowrap">
    <day 
       :currentDay="currentDay"          
          v-for="currentDay in $store.state.currentTrip.days"
          :key="currentDay.id">
  </day>
  </b-row>
</b-container>

</template>

<script>
    import Day from '@/components/Day.vue'

    export default {
      components: {
        'day': Day
      }
    }
</script>

<style lang="scss" scoped>
</style>