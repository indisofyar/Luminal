<template>
  <section class="relative overflow-hidden">

    <!-- Bg gradient -->
    <div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-gray-800 to-gray-900 opacity-60 h-[10rem] pointer-events-none -z-10" aria-hidden="true"></div>

    <!-- Illustration -->
    <div class="absolute left-1/2 -translate-x-1/2 pointer-events-none -z-10" aria-hidden="true">
      <img src="../images/hero-illustration.svg" class="max-w-none" width="2143" height="737" alt="Hero Illustration">
    </div>

    <div class="relative max-w-6xl mx-auto px-4 sm:px-6">
      <div class="pt-32 pb-12 md:pt-40 md:pb-20">

        <!-- Hero content -->
        <div class="max-w-xl mx-auto md:max-w-[640px] md:mx-0 text-center md:text-left">

          <div data-aos="zoom-out">
            <div class="relative text-sm text-gray-300 bg-gray-800 rounded-full inline-block px-4 py-1 mb-6 before:content-[''] before:absolute before:-z-10 before:inset-0 before:-m-0.5 before:bg-gradient-to-t before:from-gray-800 before:to-gray-800 before:via-gray-600 before:rounded-full">
              <div class="text-gray-400">API version 0.0.1 out now</div>
            </div>
          </div>
          <h1 class="h1 font-uncut-sans mb-6" data-aos="zoom-out" data-aos-delay="100">Understand XRPL data <em class="font-italic">seamlessly</em></h1>
          <p class="text-xl text-gray-400 mb-10" data-aos="zoom-out" data-aos-delay="200">Luminal is a comprehensive API and connector for XRPL EVM Sidechain. It enables users to easily interface with smart contract data and understand their users to a greater degree.</p>
          <div class="max-w-xs mx-auto sm:max-w-none sm:flex sm:justify-center md:justify-start space-y-4 sm:space-y-0 sm:space-x-4" data-aos="zoom-out" data-aos-delay="300">
            <div>
              <a class="btn text-white bg-gradient-to-t from-blue-600 to-blue-400 hover:to-blue-500 w-full shadow-lg group" href="https://luminal-production.up.railway.app/">
                View docs <span class="tracking-normal text-blue-200 group-hover:translate-x-0.5 transition-transform duration-150 ease-in-out ml-1">-&gt;</span>
              </a>
            </div>
            <div>
              <router-link class="btn text-gray-300 bg-gradient-to-t from-gray-800 to-gray-700 hover:to-gray-800 w-full shadow-lg" to="/demo">View Demo</router-link>
            </div>
          </div>

        </div>

      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'Hero',
}
</script>