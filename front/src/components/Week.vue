<template>
<b-container style="width: 100%; text-align: left; overflow-x: scroll">
  <b-row class="flex-nowrap">
    <day 
       :currentDay="currentDay"          
       :dayNumber=index
       v-for="(currentDay, index) in $store.state.currentTrip.days"
       :key="currentDay.id"
       v-on="$listeners"
       >
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