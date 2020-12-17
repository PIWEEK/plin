<template>
<div
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
    :img-src="plan.url_picture ? plan.url_picture : '/logo.png'" 
    img-alt="Plan picture" 
    img-left class="w-100 drag-el" 
    style="height: 4rem; margin-top:0.2rem; pointer-events: none;"    
    >
    <b-card-text>
      <div>
        {{ plan.name }}
      </div>
      <div>
        <div v-if="plan.min_price !== undefined">{{ plan.price_min }}</div>
        <div v-else style="color: white">.</div>
      </div>
      <div style="width: 100%">
        <div style="width: 85%; display: inline-block">🕑 {{ plan.duration }}h</div>
        <div style="width: 15%; display: inline-block; text-align: center"><b-img :src="gravatar('pablo.alba@kaleidos.net')" style="height:1.1rem;" rounded="circle"></b-img></div>
      </div>

    </b-card-text>
  </b-card>
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
        }
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
  margin-left: 3px;
  line-height: 1.2rem;
  text-overflow: ellipsis;
}

.card-img-left {
  border-right: 4px solid #7f7dd2;
  width: 4rem;
}

.drag-el {
    cursor: grab;
  }
</style>