<template>
<b-col style="padding: 0 0.3rem 0 0">
  <b-button style="width: 12rem">{{ currentDay.name }}</b-button>
  <div 
  class="day drop-zone"
  @drop='onDrop($event, 1)' 
  @dragover.prevent
  @dragenter.prevent
  >
   <plan-card
          :plan="plan"
          v-for="plan in currentDay.plans"
          :key="plan.id"
          v-on:plan_drop_on_child="planDropOnChild"
        ></plan-card>
  </div>
</b-col>
</template>

<script>
    import PlanCard from '@/components/PlanCard.vue'

    export default {
      components: {
        'plan-card': PlanCard
      },
      props: ["currentDay"],
      methods: {
        onDrop (evt) {
          const plan = evt.dataTransfer.getData('planId');
          console.log("onDrop "+plan);
        },
        planDropOnChild (planId, position) {          
          console.log("planDropOnChild: " + planId+ " - position: "+position);
        }
      }
    }
</script>

<style lang="scss" scoped>
.day {
  width: 12rem;
  background-color: lightgray;
  height: 40rem;
  margin-top: 0.5rem;
}

</style>