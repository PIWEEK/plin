<template>
<b-col style="padding: 0 0.3rem 0 0">
  <div class="day-header text-secondary" variant="white" style="width: 12rem">
    Día {{ dayNumber + 1 }}
  </div>
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
          v-on="$listeners"
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
        async movePlan(planId, beforePlan){
          this.$store.commit("SET_SHOWSPINNER", true);
          await this.$store.dispatch("movePlan", {"planId": planId, "dayId": this.currentDay.id, "beforePlan": beforePlan});
          await this.$store.dispatch("fetchTrip");
          this.$store.commit("SET_SHOWSPINNER", false);
        },
        onDrop (evt) {
          const planId = evt.dataTransfer.getData('planId');
          this.movePlan(planId, null);
        },
        planDropOnChild (planId, beforePlan) {    
          this.movePlan(planId, beforePlan);
        }
      }
    }
</script>

<style lang="scss" scoped>
.day-header {
  font-weight: bold;
  padding: 0.375rem 0.75rem;
  text-align: center;
}
.day {
  width: 12rem;
  background-color: #E4F5FA;
  border-radius: 4px;
  height: 40rem;
  margin-top: 0.5rem;
  padding: 10px 2px;
}

</style>