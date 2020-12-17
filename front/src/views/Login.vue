<template>
<b-container>  
  <b-container v-if="isLogin">
    <b-row>
      <b-col>
        <div style="width: 100%; height: 60rem; background: url(/petra.png); font-size:5rem; color: white; display: table;">
        <div style="display: table-cell; vertical-align: middle; padding: 2rem">
          <div>
            "{{ selectedPhraseLogin }}"
          </div>
        </div>        
        </div>
      </b-col>
      <b-col>
        <div class="text-center" style="margin-top: 6rem;">
          <b-img src="/logo.png" alt="Plin" style="width: 6rem; margin-right: 1rem"></b-img>
        </div>
        <div class="text-center" style="font-size: 2.5rem">
          ¡Hola de nuevo!
        </div>
        <b-alert v-model="showError" variant="danger" dismissible>
            Usuario / contraseña incorrectos
          </b-alert>
          <b-form @submit="onSubmit">
            <b-form-group
              id="input-group-1"
              type="email"
              label="Email:"
              label-for="input-username"
            >
              <b-form-input
                id="input-username"
                v-model="form.username"
                type="text"
                placeholder="tucorreo@mail.com"
                required
              ></b-form-input>
            </b-form-group>

            <b-form-group id="input-group-2" label="Contraseña:" label-for="input-password">
              <b-form-input
                type="password"
                id="input-password"
                v-model="form.password"
                placeholder="*****"
                required
              ></b-form-input>
            </b-form-group>

            <b-row>
              <b-col>
                <b-form-checkbox
                  id="checkbox-1"
                  v-model="form.remember"
                  name="checkbox-1"
                  value="accepted"
                  unchecked-value="not_accepted"
                >
                  Recordarme
                </b-form-checkbox>
              </b-col>
              <b-col class="text-right">
                <b-link href="#">Olvidé mi contraseña</b-link>
              </b-col>
            </b-row>
            <b-form-group id="input-group-4" style="margin-top:2rem">
              <b-button variant="primary" type="submit" style="width:100%">Entrar</b-button>
            </b-form-group>
            <b-col class="text-center">
              Aún no tengo cuenta. <b-link href="#" v-on:click="setIsLogin">Crear una</b-link>
            </b-col>
          </b-form>
      </b-col>
    </b-row>
  </b-container>
  <b-container v-else>
    <b-row>
      <b-col>
        <div style="width: 100%; height: 60rem; background: url(/turista.png); font-size:5rem; color: white; display: table;">
        <div style="display: table-cell; vertical-align: bottom; padding: 2rem">
          <div>
            "{{ selectedPhraseRegister }}"
          </div>
        </div>        
        </div>
      </b-col>
      <b-col>
        <div class="text-center" style="margin-top: 6rem;">
          <b-img src="/logo.png" alt="Plin" style="width: 6rem; margin-right: 1rem"></b-img>
        </div>
        <div class="text-center" style="font-size: 2.5rem; margin-bottom: 2rem">
          ¡Qué bien que te unas!
        </div>
        <b-alert v-model="showError" variant="danger" dismissible>
            Error en el registro
          </b-alert>
          <b-form @submit="onRegisterSubmit">
            <b-form-group
              id="input-group-2"
              label="Nombre:"
              label-for="input-name"
            >
              <b-form-input
                id="input-name"
                v-model="form.name"
                placeholder="Escribe tu nombre"
                required
              ></b-form-input>
            </b-form-group>
            <b-form-group
              id="input-group-1"
              type="email"
              label="Email:"
              label-for="input-username"
            >
              <b-form-input
                id="input-username"
                v-model="form.username"
                type="text"
                placeholder="Escribe tu correo electrónico"
                required
              ></b-form-input>
            </b-form-group>

            <b-form-group id="input-group-2" label="Contraseña:" label-for="input-password" description="Mínimo 8 caracteres">
              <b-form-input
                type="password"
                id="input-password"
                v-model="form.password"
                placeholder="Pueden ser números y letras"
                required
              ></b-form-input>
            </b-form-group>

             <b-form-group id="input-group-2" label="Confirma contraseña:" label-for="input-password">
              <b-form-input
                type="password"
                id="input-password"
                v-model="form.password2"
                placeholder="Vuelve a escribir la contraseña"
                required
              ></b-form-input>
            </b-form-group>

            

            <div>
                <b-form-checkbox
                  id="checkbox-1"
                  v-model="form.remember"
                  name="checkbox-1"
                  value="accepted"
                  unchecked-value="not_accepted"
                >
                  Recordarme
                </b-form-checkbox>
            </div>
            <b-form-group id="input-group-4" style="margin-top:2rem">
              <b-button variant="primary" type="submit" style="width:100%">Crear cuenta</b-button>
            </b-form-group>
            <b-col class="text-center">
              Ya tengo cuenta. <b-link href="#" v-on:click="setIsLogin">Entrar</b-link>
            </b-col>
          </b-form>
      </b-col>
    </b-row>
  </b-container>
</b-container>
</template>

<script>
  export default {
    data() {
      return {
        form: {
          username: '',
          email: '',
          password: '',
          password2: '',
          name: '',          
          remember: false
        },
        showError: false,
        isLogin: true,
        phrases: [
          "y te montas tu viaje en un PLÍN",
          "¿Planificar un viaje entre 8? A mi, PLÍN",
          "Y en un PLÍN, ya tenemos el viaje",
          "¿5 ciudades en tres días? A mi, PLÍN",
          "¿Gastroturismo o viaje con niños? A mi, PLÍN"
        ],
        selectedPhraseLogin: '',
        selectedPhraseRegister: '',
      }
    },
    created() {
      var idx = Math.floor(Math.random() * this.phrases.length);
      this.selectedPhraseLogin = this.phrases[idx];
      idx = Math.floor(Math.random() * this.phrases.length);
      this.selectedPhraseRegister = this.phrases[idx];
    },
    methods: {
      async onSubmit(event) {
        event.preventDefault();
        this.$store.commit("SET_SHOWSPINNER", true);
        this.form.email = this.form.username;
        const response = await this.$store.dispatch("login", JSON.stringify(this.form));
        const token = response.access;
        this.$store.commit("SET_SHOWSPINNER", false);
        if (token === undefined){
          this.showError = true;          
        } else {
          this.$store.commit('SET_CURRENTUSER', {username: this.form.username, token: token});          
          this.$router.push("/home");
        }
      },
      async onRegisterSubmit(event) {
        event.preventDefault();
        this.form.email = this.form.username;
        const response = await this.$store.dispatch("register", JSON.stringify(this.form));
        const email = response.email;
        if (email === undefined){
          this.showError = true
        } else {
          this.onSubmit(event);
        }
      },
      setIsLogin(event){
        event.preventDefault();
        this.isLogin = !this.isLogin;
      }
    }
  }
</script>

<style lang="scss" scoped>
.btn-primary {
	color: #fff;
	background-color: #97d6e0;
	border-color: #97d6e0;
}

.btn-primary:hover {
	color: #fff;
	background-color: #53cde0;
	border-color: #53cde0;
}
</style>


