<template>
<div
  class="plancard"
  v-on:click='onClick'
  draggable
  @drop='onDrop($event, 1)'
  @dragstart='startDrag($event)'
  @dragover.prevent
  @dragleave='dragLeave($event)'
  @dragenter='dragEnter($event)'>
  <div v-if="isDraggingOnMe" style="height: 4rem; border: 1px dashed black; pointer-events: none;">
  </div>
  <b-card
    :img-src="plan.url_picture"
    img-alt="Plan picture"
    img-left
    class="w-100 drag-el"
    :class="plan.plan_type"
    style="height: 4rem; margin-top:0.2rem; pointer-events: none;"
    >
    <b-card-text>
      <div class="name">
        {{ plan.name }}
      </div>
      <div>
        <div v-if="plan.price_min || plan.price_max ">
          <span v-if="plan.price_min">{{ plan.price_min }}</span>
          <span v-if="plan.price_min && plan.price_max"> - </span>
          <span v-if="plan.price_max">{{ plan.price_max }}</span>
        </div>
        <div v-else style="color: white">.</div>
      </div>
      <div style="width: 100%; padding-right: 2px;">
        <div style="width: 80%; display: inline-block">🕑 {{ plan.duration }}h</div>
        <div style="width: 20%; display: inline-block; text-align: right; position: relative; top: -0.2rem; left: -0.2rem"><b-img :src="gravatar(plan.created_by.email)" style="height:1.1rem;" rounded="circle"></b-img></div>
      </div>


    </b-card-text>

  </b-card>

  <div class="card_buttons" style="position: absolute; top: 4px; right:4px">
    <b-link href="#" v-on:click="onDeletePlan" style="padding-right: 4px">
      <b-img src="/delete.png"></b-img>
    </b-link>
    <b-link href="#" v-on:click="onDuplicatePlan">
      <b-img src="/duplicate.png"></b-img>
    </b-link>
  </div>
</div>
</template>

<script>
    export default {
      props: ["plan"],
      data() {
        return {
          draggingOnMe:  false
        };
      },
      computed: {
        isDraggingOnMe(){
          return this.draggingOnMe;
        }
      },
      methods: {
        startDrag(evt) {
          evt.dataTransfer.dropEffect = 'move';
          evt.dataTransfer.effectAllowed = 'move';
          evt.dataTransfer.setData('planId', this.plan.id);
        },
        dragEnter() {
          this.draggingOnMe = true;
        },
        dragLeave() {
          this.draggingOnMe = false;
        },
        onDrop (evt) {
          evt.stopPropagation();
          this.draggingOnMe = false;
          const plan = evt.dataTransfer.getData('planId');
          console.log("Drop over card "+plan);
          this.$emit('plan_drop_on_child', plan, this.plan.id);
        },
        gravatar(email) {
          var md5 = require('md5');
          const hash = md5(email)
          return "http://www.gravatar.com/avatar/"+hash;
        },
        onClick(){
          this.$emit('edit_plan', JSON.stringify(this.plan));
        },
        onDeletePlan(evt){
          evt.stopPropagation();
          this.$bvModal.msgBoxConfirm("¿Seguro que quieres borrar el plan \""+this.plan.name+"\"?").then(value => {
            if(value){
              this.deletePlan();
            }
          });
        },
        async deletePlan(){
          this.$store.commit("SET_SHOWSPINNER", true);
          await this.$store.dispatch("deletePlan",this.plan.id);
          await this.$store.dispatch("fetchTrip");
          this.$store.commit("SET_SHOWSPINNER", false);
        },
        onDuplicatePlan(evt){
          evt.stopPropagation();
          this.$bvModal.msgBoxConfirm("¿Seguro que quieres duplicar el plan \""+this.plan.name+"\"?").then(value => {
            if(value){
              this.duplicatePlan();
            }
          });
        },
        async duplicatePlan(){
          this.$emit('duplicate_plan', JSON.stringify(this.plan));
        },
      }
    }
</script>

<style lang="scss" scoped>
.card-body {
  padding: 0.3rem 0 0 0.1rem;
  flex: 0.1 1 auto;
  font-size: 14px;
  text-align: left;
  white-space: nowrap;
  width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card-text {
  margin-left: 0.3rem;
  line-height: 1.2rem;
  text-overflow: ellipsis;
}

.Culture .card-img-left {
  border-right: 0.2rem solid #FFF8A6;
  width: 4rem;
}

.Gastronomy .card-img-left {
  border-right: 0.2rem solid #F08A8A;
  width: 4rem;
}

.Walk .card-img-left {
  border-right: 0.2rem solid #9FC7EB;
  width: 4rem;
}

.Nature .card-img-left {
  border-right: 0.2rem solid #B8DFC1;
  width: 4rem;
}

.Other .card-img-left {
  border-right: 0.2rem solid #F2BB8B;
  width: 4rem;
}

.drag-el {
  cursor: grab;
}

.plancard {
  cursor: grab;
  position: relative;
}

.plancard .card_buttons {
  display: none;
}

.plancard:hover .card_buttons {
  display: block;
  cursor: pointer;
}

.plancard .card_buttons img{
  width: 1.5rem;
}

.name {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-weight: bold;
}

</style>