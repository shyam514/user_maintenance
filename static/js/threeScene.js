// Three.js Background Scene Setup
document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.querySelector('#bg-canvas');
    if (!canvas) return;

    // Scene setup
    const scene = new THREE.Scene();
    // Use a dark slate background to match the theme
    scene.background = new THREE.Color(0x0f172a);
    
    // Camera setup
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 30;
    
    // Renderer setup
    const renderer = new THREE.WebGLRenderer({
        canvas: canvas,
        antialias: true,
        alpha: true
    });
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(window.innerWidth, window.innerHeight);
    
    // Add Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);
    
    const pointLight1 = new THREE.PointLight(0xa855f7, 2, 100);
    pointLight1.position.set(20, 20, 20);
    scene.add(pointLight1);
    
    const pointLight2 = new THREE.PointLight(0xec4899, 2, 100);
    pointLight2.position.set(-20, -20, 20);
    scene.add(pointLight2);
    
    const pointLight3 = new THREE.PointLight(0x6366f1, 2, 100);
    pointLight3.position.set(0, 0, 50);
    scene.add(pointLight3);
    
    // Create Glass Material
    const glassMaterial = new THREE.MeshPhysicalMaterial({
        color: 0xffffff,
        metalness: 0.1,
        roughness: 0.1,
        transmission: 0.9, // glass-like
        thickness: 0.5,
        clearcoat: 1.0,
        clearcoatRoughness: 0.1,
        ior: 1.5,
        transparent: true,
        opacity: 0.8
    });
    
    // Create Crystal Material (more reflective and colorful)
    const crystalMaterial = new THREE.MeshPhysicalMaterial({
        color: 0xe0e7ff,
        metalness: 0.3,
        roughness: 0.2,
        transmission: 0.8,
        thickness: 1.0,
        clearcoat: 1.0,
        ior: 2.4, // diamond-like
        transparent: true,
        opacity: 0.9
    });
    
    // Objects Array to hold meshes for animation
    const objects = [];
    
    // 1. Floating Glass Spheres
    const sphereGeometry = new THREE.SphereGeometry(1, 32, 32);
    for (let i = 0; i < 15; i++) {
        const sphere = new THREE.Mesh(sphereGeometry, glassMaterial);
        
        // Random position
        sphere.position.x = (Math.random() - 0.5) * 60;
        sphere.position.y = (Math.random() - 0.5) * 60;
        sphere.position.z = (Math.random() - 0.5) * 40 - 10;
        
        // Random scale
        const scale = Math.random() * 2 + 0.5;
        sphere.scale.set(scale, scale, scale);
        
        // Store random rotation and movement speeds
        sphere.userData = {
            rotSpeed: {
                x: (Math.random() - 0.5) * 0.02,
                y: (Math.random() - 0.5) * 0.02,
                z: (Math.random() - 0.5) * 0.02
            },
            moveSpeed: {
                y: (Math.random() - 0.5) * 0.05
            },
            originalY: sphere.position.y
        };
        
        scene.add(sphere);
        objects.push(sphere);
    }
    
    // 2. Rotating Transparent Cubes / Crystals
    const boxGeometry = new THREE.BoxGeometry(2, 2, 2);
    const octahedronGeometry = new THREE.OctahedronGeometry(2);
    
    for (let i = 0; i < 10; i++) {
        const geometry = Math.random() > 0.5 ? boxGeometry : octahedronGeometry;
        const crystal = new THREE.Mesh(geometry, crystalMaterial);
        
        crystal.position.x = (Math.random() - 0.5) * 60;
        crystal.position.y = (Math.random() - 0.5) * 60;
        crystal.position.z = (Math.random() - 0.5) * 40 - 20;
        
        const scale = Math.random() * 1.5 + 0.5;
        crystal.scale.set(scale, scale, scale);
        
        crystal.userData = {
            rotSpeed: {
                x: (Math.random() - 0.5) * 0.03,
                y: (Math.random() - 0.5) * 0.03,
                z: (Math.random() - 0.5) * 0.03
            },
            moveSpeed: {
                y: (Math.random() - 0.5) * 0.03
            },
            originalY: crystal.position.y
        };
        
        scene.add(crystal);
        objects.push(crystal);
    }
    
    // Mouse Interaction
    let mouseX = 0;
    let mouseY = 0;
    let targetX = 0;
    let targetY = 0;
    const windowHalfX = window.innerWidth / 2;
    const windowHalfY = window.innerHeight / 2;
    
    document.addEventListener('mousemove', (event) => {
        mouseX = (event.clientX - windowHalfX) * 0.05;
        mouseY = (event.clientY - windowHalfY) * 0.05;
    });
    
    // Animation Loop
    const clock = new THREE.Clock();
    
    function animate() {
        requestAnimationFrame(animate);
        
        const elapsedTime = clock.getElapsedTime();
        
        // Smooth camera movement based on mouse
        targetX = mouseX * 0.5;
        targetY = mouseY * 0.5;
        
        camera.position.x += (targetX - camera.position.x) * 0.02;
        camera.position.y += (-targetY - camera.position.y) * 0.02;
        camera.lookAt(scene.position);
        
        // Animate objects
        objects.forEach(obj => {
            // Rotation
            obj.rotation.x += obj.userData.rotSpeed.x;
            obj.rotation.y += obj.userData.rotSpeed.y;
            obj.rotation.z += obj.userData.rotSpeed.z;
            
            // Floating motion
            obj.position.y = obj.userData.originalY + Math.sin(elapsedTime * 0.5 + obj.position.x) * 2;
        });
        
        // Move lights slightly
        pointLight1.position.x = Math.sin(elapsedTime * 0.5) * 30;
        pointLight1.position.z = Math.cos(elapsedTime * 0.5) * 30;
        
        pointLight2.position.y = Math.sin(elapsedTime * 0.3) * 30;
        pointLight2.position.x = Math.cos(elapsedTime * 0.3) * 30;
        
        renderer.render(scene, camera);
    }
    
    animate();
    
    // Handle Window Resize
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
});
