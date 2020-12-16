<template>
<div
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
    img-left class="w-100 drag-el" 
    style="height: 4rem; margin-top:0.2rem; pointer-events: none;"    
    >
    <b-card-text>
    <div>
      {{ plan.title }}
    </div>
    <div>
      <span v-if="plan.price !== null">{{ plan.price }}</span>
      <span v-else>&nbsp;</span>
    </div>
    <div>
      <span v-if="plan.duration !== null">🕑 {{ plan.duration }}</span>
      <span v-else>&nbsp;</span>
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
          this.$emit('plan_drop_on_child', plan, this.plan.position);
        }
      }
    }
</script>

<style lang="scss" scoped>
.card-body {
  padding: 0.3rem 0 0 0;
  flex: 0.1 1 auto;
  font-size: 14px;
  text-align: left;
}

.card-text {
  margin-left: 3px;  
}

.card-img-left {
  border-right: 4px solid blue;
  width: 4rem;
}

.drag-el {
    cursor: grab;
  }
</style>