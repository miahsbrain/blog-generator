document.addEventListener('alpine:init', function(){
    Alpine.store('lsidebar', {
        'open': false,
        toggle() {
            this.open = !this.open
        },
        on(){
            this.open = true
        },
        off(){
            this.open = false
        }
    })
})