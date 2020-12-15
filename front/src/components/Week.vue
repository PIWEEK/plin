<template>
<div style="width: 100%; overflow-x: scroll">
  <day 
       :currentDay="currentDay"          
          v-for="currentDay in $store.state.currentTrip.days"
          :key="currentDay.id">
  </day>
</div>
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