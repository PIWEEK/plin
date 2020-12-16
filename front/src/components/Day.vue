<template>
<b-col style="padding: 0 0.3rem 0 0">
  <b-button style="width: 12rem">Día {{ dayNumber + 1 }}</b-button>
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
      props: ["currentDay", "dayNumber"],
      methods: {
        async movePlan(planId){
          this.$store.commit("SET_SHOWSPINNER", true);
          await this.$store.dispatch("movePlan", {"planId": planId, "dayId": this.currentDay.id});
          await this.$store.dispatch("fetchTrip");
          this.$store.commit("SET_SHOWSPINNER", false);
        },
        onDrop (evt) {
          const planId = evt.dataTransfer.getData('planId');
          console.log("onDrop "+planId);
          this.movePlan(planId);
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