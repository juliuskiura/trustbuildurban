from django.core.management.base import BaseCommand
from available_homes.models import (
    AvailableHome,
    BathroomInformation,
    BedroomInformation,
    HeatingAndCooling,
    KitchenAndDining,
    InteriorFeatures,
    OtherRooms,
    GarageAndParking,
    UtilitiesAndGreenEnergy,
    OutdoorSpaces,
)


class Command(BaseCommand):
    help = 'Populate property details for all available homes with comprehensive data'

    def handle(self, *args, **kwargs):
        homes = AvailableHome.objects.all()
        
        if not homes.exists():
            self.stdout.write(self.style.WARNING('No available homes found. Please create homes first.'))
            return

        self.stdout.write(f'Found {homes.count()} homes. Populating detailed information...')

        for home in homes:
            # Clear existing data for this home
            BathroomInformation.objects.filter(home=home).delete()
            BedroomInformation.objects.filter(home=home).delete()
            HeatingAndCooling.objects.filter(home=home).delete()
            KitchenAndDining.objects.filter(home=home).delete()
            InteriorFeatures.objects.filter(home=home).delete()
            OtherRooms.objects.filter(home=home).delete()
            GarageAndParking.objects.filter(home=home).delete()
            UtilitiesAndGreenEnergy.objects.filter(home=home).delete()
            OutdoorSpaces.objects.filter(home=home).delete()

            # Populate based on home characteristics
            if "Sapphire" in home.title:
                self.populate_luxury_penthouse(home)
            elif "Veranda" in home.title:
                self.populate_modern_suite(home)
            elif "Garden" in home.title:
                self.populate_family_estate(home)
            elif "Loft" in home.title:
                self.populate_urban_loft(home)
            elif "Palm" in home.title:
                self.populate_desert_modern(home)
            elif "Willow" in home.title:
                self.populate_suburban_home(home)
            else:
                self.populate_default(home)

        self.stdout.write(self.style.SUCCESS(f'Successfully populated detailed information for {homes.count()} homes'))

    def populate_luxury_penthouse(self, home):
        """The Sapphire Residence - Luxury penthouse in the city"""
        # Bathrooms
        BathroomInformation.objects.create(home=home, title="Master Bathroom", value="Spa-like master bath with heated floors, double vanities, soaking tub, rainfall shower, smart mirror")
        BathroomInformation.objects.create(home=home, title="Bathroom 2", value="En-suite to bedroom 2 - Walk-in shower, single vanity")
        BathroomInformation.objects.create(home=home, title="Bathroom 3", value="En-suite to bedroom 3 - Full bath with tub")
        BathroomInformation.objects.create(home=home, title="Guest Bathroom", value="Half bath - Designer fixtures, decorative mirror")
        BathroomInformation.objects.create(home=home, title="Powder Room", value="Elegant powder room with pedestal sink")

        # Bedrooms
        BedroomInformation.objects.create(home=home, title="Master Bedroom", value="25x20 - Panoramic city views, private balcony, walk-in closet, smart lighting")
        BedroomInformation.objects.create(home=home, title="Bedroom 2", value="18x14 - City views, walk-in closet, en-suite bath")
        BedroomInformation.objects.create(home=home, title="Bedroom 3", value="16x14 - Corner unit, abundant natural light")
        BedroomInformation.objects.create(home=home, title="Home Office", value="14x12 - Built-in desk, soundproof walls, high-speed internet")

        # Heating/Cooling
        HeatingAndCooling.objects.create(home=home, title="Heating", value="Central heating - Multi-zone radiant floor heating system")
        HeatingAndCooling.objects.create(home=home, title="Cooling", value="Central AC - VRF system with individual room controls")
        HeatingAndCooling.objects.create(home=home, title="Fireplace", value="Living room - Bioethanol fireplace with remote")

        # Kitchen
        KitchenAndDining.objects.create(home=home, title="Kitchen", value="Chef's kitchen - Marble countertops, 12ft island, custom Italian cabinets")
        KitchenAndDining.objects.create(home=home, title="Appliances", value="Sub-Zero refrigerator, Wolf range, Miele dishwasher, wine cooler")
        KitchenAndDining.objects.create(home=home, title="Pantry", value="Butler's pantry with additional storage and prep area")
        KitchenAndDining.objects.create(home=home, title="Dining", value="Formal dining - 12-person table space, custom chandelier")

        # Interior
        InteriorFeatures.objects.create(home=home, title="Flooring", value="Italian marble throughout, wool carpet in bedrooms")
        InteriorFeatures.objects.create(home=home, title="Ceilings", value="12-foot ceilings, coffered details in living areas")
        InteriorFeatures.objects.create(home=home, title="Smart Home", value="Full Crestron automation - Lights, climate, audio, security")
        InteriorFeatures.objects.create(home=home, title="Windows", value="Floor-to-ceiling windows with automatic blinds")
        InteriorFeatures.objects.create(home=home, title="Laundry", value="In-unit laundry - Full size washer/dryer, sink, cabinetry")

        # Other Rooms
        OtherRooms.objects.create(home=home, title="Living Room", value="35x22 - Double-height ceilings, floor-to-ceiling windows, city views")
        OtherRooms.objects.create(home=home, title="Media Room", value="Home theater with 4K projector, surround sound")
        OtherRooms.objects.create(home=home, title="Foyer", value="Grand entrance with gallery wall space, built-in storage")

        # Garage
        GarageAndParking.objects.create(home=home, title="Parking", value="2 dedicated parking spaces in secure garage")
        GarageAndParking.objects.create(home=home, title="Storage", value="Climate-controlled storage unit included")

        # Utilities
        UtilitiesAndGreenEnergy.objects.create(home=home, title="Water", value="City water with filtration system")
        UtilitiesAndGreenEnergy.objects.create(home=home, title="Energy", value="Energy-efficient building, LED lighting throughout")
        UtilitiesAndGreenEnergy.objects.create(home=home, title="Security", value="24/7 concierge, secure entry, cameras")

        # Outdoor
        OutdoorSpaces.objects.create(home=home, title="Private Terrace", value="800 sq ft terrace with city views, outdoor seating, BBQ area")
        OutdoorSpaces.objects.create(home=home, title="Building Amenities", value="Rooftop pool, fitness center, residents lounge, wine cellar")

    def populate_modern_suite(self, home):
        """Veranda Suites - Modern urban living"""
        # Bathrooms
        BathroomInformation.objects.create(home=home, title="Master Bathroom", value="Modern design, glass-enclosed shower, floating vanity")
        BathroomInformation.objects.create(home=home, title="Bathroom 2", value="Full bath with tub/shower combo")
        BathroomInformation.objects.create(home=home, title="Guest Bathroom", value="Half bath with modern fixtures")

        # Bedrooms
        BedroomInformation.objects.create(home=home, title="Master Bedroom", value="18x16 - Walk-in closet, en-suite bath, workspace corner")
        BedroomInformation.objects.create(home=home, title="Bedroom 2", value="14x12 - Closet, adjacent to full bath")
        BedroomInformation.objects.create(home=home, title="Den", value="10x10 - Can serve as office or guest room")

        # Heating/Cooling
        HeatingAndCooling.objects.create(home=home, title="Climate", value="Central AC/heat with programmable thermostat")
        HeatingAndCooling.objects.create(home=home, title="Ventilation", value="Heat recovery ventilator for fresh air")

        # Kitchen
        KitchenAndDining.objects.create(home=home, title="Kitchen", value="Open concept - Quartz counters, modern cabinets, breakfast bar")
        KitchenAndDining.objects.create(home=home, title="Appliances", value="Stainless steel - Fridge, oven, dishwasher, microwave")
        KitchenAndDining.objects.create(home=home, title="Dining", value="Open to living area, space for 6-person table")

        # Interior
        InteriorFeatures.objects.create(home=home, title="Flooring", value="Wide-plank oak flooring, tile in baths")
        InteriorFeatures.objects.create(home=home, title="Smart Home", value="Smart locks, thermostat, lighting control")
        InteriorFeatures.objects.create(home=home, title="Laundry", value="In-unit washer/dryer")

        # Other Rooms
        OtherRooms.objects.create(home=home, title="Living Room", value="Open concept with city views")
        OtherRooms.objects.create(home=home, title="Entry", value="Foyer with coat closet")

        # Garage
        GarageAndParking.objects.create(home=home, title="Parking", value="1 secured parking space included")

        # Utilities
        UtilitiesAndGreenEnergy.objects.create(home=home, title="Utilities", value="Gas, electric, water included in HOA")
        UtilitiesAndGreenEnergy.objects.create(home=home, title="Security", value="Key card access, video intercom")

        # Outdoor
        OutdoorSpaces.objects.create(home=home, title="Balcony", value="Private balcony - 60 sq ft, outdoor furniture space")
        OutdoorSpaces.objects.create(home=home, title="Common Areas", value="Courtyard garden, rooftop deck, BBQ area")

    def populate_family_estate(self, home):
        """The Garden Estate - Large family home"""
        # Bathrooms
        BathroomInformation.objects.create(home=home, title="Master Bathroom", value="Luxury spa - Double vanities, jetted tub, rainfall shower, heated floors")
        BathroomInformation.objects.create(home=home, title="Bathroom 2", value="Jack and Jill bath connecting bedrooms 2 and 3")
        BathroomInformation.objects.create(home=home, title="Bathroom 3", value="En-suite to bedroom 4")
        BathroomInformation.objects.create(home=home, title="Bathroom 4", value="Full bath near bonus room")
        BathroomInformation.objects.create(home=home, title="Powder Room", value="Elegant main floor powder room")
        BathroomInformation.objects.create(home=home, title="Pool Bath", value="Half bath by pool area")

        # Bedrooms
        BedroomInformation.objects.create(home=home, title="Master Suite", value="22x18 - Sitting area, dual walk-in closets, fireplace")
        BedroomInformation.objects.create(home=home, title="Bedroom 2", value="16x14 - Walk-in closet, bay window")
        BedroomInformation.objects.create(home=home, title="Bedroom 3", value="15x13 - Closet, garden view")
        BedroomInformation.objects.create(home=home, title="Bedroom 4", value="14x12 - Standard closet")
        BedroomInformation.objects.create(home=home, title="Bedroom 5", value="14x12 - Currently used as home office")
        BedroomInformation.objects.create(home=home, title="Nursery", value="12x11 - Connected to master suite")

        # Heating/Cooling
        HeatingAndCooling.objects.create(home=home, title="Heating", value="Dual-zone gas furnace, radiant heat in master bath")
        HeatingAndCooling.objects.create(home=home, title="Cooling", value="Dual-zone central AC")
        HeatingAndCooling.objects.create(home=home, title="Fireplaces", value="Master bedroom and family room - Gas")

        # Kitchen
        KitchenAndDining.objects.create(home=home, title="Main Kitchen", value="Gourmet kitchen - 6-burner gas range, double ovens, large island")
        KitchenAndDining.objects.create(home=home, title="Countertops", value="Granite with marble island")
        KitchenAndDining.objects.create(home=home, title="Pantry", value="Walk-in pantry plus butler's pantry")
        KitchenAndDining.objects.create(home=home, title="Breakfast Nook", value="Bay window nook overlooking garden")
        KitchenAndDining.objects.create(home=home, title="Kitchen 2", value="Secondary kitchen/bar in basement")

        # Interior
        InteriorFeatures.objects.create(home=home, title="Flooring", value="Hardwood main level, carpet upstairs, tile wet areas")
        InteriorFeatures.objects.create(home=home, title="Ceilings", value="10ft main floor, 9ft upstairs, vaulted in family room")
        InteriorFeatures.objects.create(home=home, title="Smart Home", value="Whole-home automation system")
        InteriorFeatures.objects.create(home=home, title="Media Room", value="Basement home theater")
        InteriorFeatures.objects.create(home=home, title="Wine Cellar", value="Temperature-controlled wine storage")
        InteriorFeatures.objects.create(home=home, title="Laundry", value="Main floor and upstairs laundry rooms")

        # Other Rooms
        OtherRooms.objects.create(home=home, title="Family Room", value="24x20 - Vaulted ceiling, fireplace, built-ins")
        OtherRooms.objects.create(home=home, title="Living Room", value="20x16 - Formal living with bay window")
        OtherRooms.objects.create(home=home, title="Dining Room", value="18x14 - Formal dining, chandelier")
        OtherRooms.objects.create(home=home, title="Office", value="Main floor private office with French doors")
        OtherRooms.objects.create(home=home, title="Bonus Room", value="Upstairs playroom/hangout space")
        OtherRooms.objects.create(home=home, title="Mudroom", value="Large mudroom with lockers, bench, dog wash")

        # Garage
        GarageAndParking.objects.create(home=home, title="Garage", value="3-car attached garage with epoxy floor")
        GarageAndParking.objects.create(home=home, title="Workshop", value="Extra deep bay for workshop/storage")
        GarageAndParking.objects.create(home=home, title="Parking", value="Circular driveway with additional parking")
        GarageAndParking.objects.create(home=home, title="EV Charging", value="EV charger installed")

        # Utilities
        UtilitiesAndGreenEnergy.objects.create(home=home, title="Solar", value="Owned solar panel system")
        UtilitiesAndGreenEnergy.objects.create(home=home, title="Water Heater", value="Two tankless water heaters")
        UtilitiesAndGreenEnergy.objects.create(home=home, title="Generator", value="Whole-house backup generator")
        UtilitiesAndGreenEnergy.objects.create(home=home, title="Security", value="Full security system with cameras")

        # Outdoor
        OutdoorSpaces.objects.create(home=home, title="Pool", value="Heated saltwater pool with spa")
        OutdoorSpaces.objects.create(home=home, title="Patio", value="Covered patio with fireplace, TV, outdoor speakers")
        OutdoorSpaces.objects.create(home=home, title="Garden", value="Mature landscaping, raised bed garden")
        OutdoorSpaces.objects.create(home=home, title="Yard", value="1-acre lot, fully fenced")
        OutdoorSpaces.objects.create(home=home, title="Sport Court", value="Half basketball court")
        OutdoorSpaces.objects.create(home=home, title="Trees", value="Mature oak and maple trees")

    def populate_urban_loft(self, home):
        """Modern Loft Apartments - Industrial chic"""
        # Bathrooms
        BathroomInformation.objects.create(home=home, title="Full Bathroom", value="Open concept bath with exposed pipes, walk-in rain shower")
        BathroomInformation.objects.create(home=home, title="Half Bathroom", value="Industrial-style half bath")

        # Bedrooms
        BedroomInformation.objects.create(home=home, title="Main Bedroom", value="Open loft bedroom with exposed brick, platform bed area")
        BedroomInformation.objects.create(home=home, title="Sleeping Loft", value="Overlooking living area - Perfect for guests")

        # Heating/Cooling
        HeatingAndCooling.objects.create(home=home, title="Climate", value="HVAC with exposed ductwork")
        HeatingAndCooling.objects.create(home=home, title="Windows", value="Industrial-style warehouse windows")

        # Kitchen
        KitchenAndDining.objects.create(home=home, title="Kitchen", value="Open kitchen - Stainless steel counters, open shelving")
        KitchenAndDining.objects.create(home=home, title="Appliances", value="Fridge, gas range, dishwasher, microwave")
        KitchenAndDining.objects.create(home=home, title="Dining", value="Open to living, bar seating at island")

        # Interior
        InteriorFeatures.objects.create(home=home, title="Walls", value="Exposed brick, concrete floors")
        InteriorFeatures.objects.create(home=home, title="Ceilings", value="16ft high exposed beam ceilings")
        InteriorFeatures.objects.create(home=home, title="Character", value="Original hardwood, industrial fixtures")
        InteriorFeatures.objects.create(home=home, title="Laundry", value="In-unit stackable washer/dryer")

        # Other Rooms
        OtherRooms.objects.create(home=home, title="Living Area", value="Open floor plan, 20ft ceilings, natural light")
        OtherRooms.objects.create(home=home, title="Workspace", value="Built-in desk area, high-speed fiber internet")

        # Garage
        GarageAndParking.objects.create(home=home, title="Parking", value="1 secured parking spot in building garage")

        # Utilities
        UtilitiesAndGreenEnergy.objects.create(home=home, title="Utilities", value="Water included, electric and gas separate")
        UtilitiesAndGreenEnergy.objects.create(home=home, title="Sustainability", value="Building uses renewable energy")

        # Outdoor
        OutdoorSpaces.objects.create(home=home, title="Rooftop", value="Common rooftop deck with city views")
        OutdoorSpaces.objects.create(home=home, title="Courtyard", value="Interior courtyard with BBQ area")

    def populate_desert_modern(self, home):
        """The Palm Springs - Desert modern architecture"""
        # Bathrooms
        BathroomInformation.objects.create(home=home, title="Master Bathroom", value="Desert spa - Indoor/outdoor shower, floating tub, mountain views")
        BathroomInformation.objects.create(home=home, title="Bathroom 2", value="Guest bath with pool access")
        BathroomInformation.objects.create(home=home, title="Outdoor Bath", value="Private outdoor shower by pool")

        # Bedrooms
        BedroomInformation.objects.create(home=home, title="Master Suite", value="20x18 - Wall of glass to pool, outdoor access")
        BedroomInformation.objects.create(home=home, title="Guest Room 1", value="Casita with private entrance - 16x14")
        BedroomInformation.objects.create(home=home, title="Guest Room 2", value="15x13 - Mountain views")
        BedroomInformation.objects.create(home=home, title="Media Room", value="Can serve as 4th bedroom")

        # Heating/Cooling
        HeatingAndCooling.objects.create(home=home, title="Cooling", value=" evaporative cooling + central AC")
        HeatingAndCooling.objects.create(home=home, title="Pool Heating", value="Solar and gas pool heating")
        HeatingAndCooling.objects.create(home=home, title="Fire Features", value="Fire pit, outdoor fireplace")

        # Kitchen
        KitchenAndDining.objects.create(home=home, title="Kitchen", value="Chef's kitchen - Walls of glass, mountain views")
        KitchenAndDining.objects.create(home=home, title="Outdoor Kitchen", value="Full outdoor kitchen with pizza oven")
        KitchenAndDining.objects.create(home=home, title="Countertops", value="Concrete counters, waterfall edge island")

        # Interior
        InteriorFeatures.objects.create(home=home, title="Architecture", value="Mid-century modern design, post-and-beam")
        InteriorFeatures.objects.create(home=home, title="Flooring", value="Terrazzo floors, concrete")
        InteriorFeatures.objects.create(home=home, title="Windows", value="Floor-to-ceiling glass walls")
        InteriorFeatures.objects.create(home=home, title="Laundry", value="Large laundry with built-in ironing station")

        # Other Rooms
        OtherRooms.objects.create(home=home, title="Living Room", value="30x20 - Walls of glass, fireplace, pool view")
        OtherRooms.objects.create(home=home, title="Casita", value="Separate guest house with kitchenette")
        OtherRooms.objects.create(home=home, title="Entry", value="Covered entry with dramatic mountain approach")

        # Garage
        GarageAndParking.objects.create(home=home, title="Garage", value="2-car garage with golf cart storage")
        GarageAndParking.objects.create(home=home, title="Carport", value="Additional covered parking")

        # Utilities
        UtilitiesAndGreenEnergy.objects.create(home=home, title="Solar", value="Owned solar array")
        UtilitiesAndGreenEnergy.objects.create(home=home, title="Water", value="Well water, drip irrigation system")
        UtilitiesAndGreenEnergy.objects.create(home=home, title="Pool", value="Saltwater pool with Pebble Tec finish")

        # Outdoor
        OutdoorSpaces.objects.create(home=home, title="Pool", value="Saltwater pool with spa - Mountain backdrop")
        OutdoorSpaces.objects.create(home=home, title="Patio", value="Covered patios - Over 2000 sq ft outdoor living")
        OutdoorSpaces.objects.create(home=home, title="Landscape", value="Desert landscaping, succulents, cacti")
        OutdoorSpaces.objects.create(home=home, title="Views", value="Panoramic mountain and sunset views")
        OutdoorSpaces.objects.create(home=home, title="Privacy", value="Private walled compound")

    def populate_suburban_home(self, home):
        """The Willow Creek - Classic suburban family home"""
        # Bathrooms
        BathroomInformation.objects.create(home=home, title="Master Bath", value="Double sinks, shower/tub combo, separate toilet room")
        BathroomInformation.objects.create(home=home, title="Full Bath 2", value="Hall bath - Tub/shower combo, single vanity")
        BathroomInformation.objects.create(home=home, title="Half Bath", value="Main floor half bath")

        # Bedrooms
        BedroomInformation.objects.create(home=home, title="Master Bedroom", value="18x16 - Walk-in closet, ceiling fan")
        BedroomInformation.objects.create(home=home, title="Bedroom 2", value="14x12 - Double closet")
        BedroomInformation.objects.create(home=home, title="Bedroom 3", value="13x11 - Single closet")
        BedroomInformation.objects.create(home=home, title="Bedroom 4", value="12x11 - Could be home office")

        # Heating/Cooling
        HeatingAndCooling.objects.create(home=home, title="Heating", value="Gas forced air furnace")
        HeatingAndCooling.objects.create(home=home, title="Cooling", value="Central AC")
        HeatingAndCooling.objects.create(home=home, title="Fireplace", value="Wood-burning fireplace in family room")

        # Kitchen
        KitchenAndDining.objects.create(home=home, title="Kitchen", value="Updates cabinets, laminate counters, island")
        KitchenAndDining.objects.create(home=home, title="Appliances", value="Electric range, fridge, dishwasher")
        KitchenAndDining.objects.create(home=home, title="Dining", value="Adjacent to kitchen, space for table")

        # Interior
        InteriorFeatures.objects.create(home=home, title="Flooring", value="Carpet, vinyl in kitchen/baths")
        InteriorFeatures.objects.create(home=home, title="Laundry", value="Main floor laundry, included washer/dryer")

        # Other Rooms
        OtherRooms.objects.create(home=home, title="Family Room", value="Large family room with fireplace")
        OtherRooms.objects.create(home=home, title="Living Room", value="Front living room, formal space")
        OtherRooms.objects.create(home=home, title="Office", value="Dedicated home office space")

        # Garage
        GarageAndParking.objects.create(home=home, title="Garage", value="2-car attached garage")
        GarageAndParking.objects.create(home=home, title="Driveway", value="Wide concrete driveway")

        # Utilities
        UtilitiesAndGreenEnergy.objects.create(home=home, title="Water Heater", value="40-gallon gas water heater")
        UtilitiesAndGreenEnergy.objects.create(home=home, title="Utilities", value="City water/sewer, electric, gas")

        # Outdoor
        OutdoorSpaces.objects.create(home=home, title="Backyard", value="Fenced backyard, large trees")
        OutdoorSpaces.objects.create(home=home, title="Patio", value="Concrete patio, room for furniture")
        OutdoorSpaces.objects.create(home=home, title="Garden", value="Garden beds, established shrubs")

    def populate_default(self, home):
        """Default data for any home"""
        # Bathrooms
        BathroomInformation.objects.create(home=home, title="Full Bathroom", value="Full bath with tub/shower")
        
        # Bedrooms
        BedroomInformation.objects.create(home=home, title="Bedroom", value="Good size with closet")
        
        # Heating/Cooling
        HeatingAndCooling.objects.create(home=home, title="Heating/Cooling", value="Central HVAC")
        
        # Kitchen
        KitchenAndDining.objects.create(home=home, title="Kitchen", value="Full kitchen with appliances")
        
        # Interior
        InteriorFeatures.objects.create(home=home, title="Features", value="Standard interior finishes")
        
        # Other Rooms
        OtherRooms.objects.create(home=home, title="Living Area", value="Open living space")
        
        # Garage
        GarageAndParking.objects.create(home=home, title="Parking", value="Parking available")
        
        # Utilities
        UtilitiesAndGreenEnergy.objects.create(home=home, title="Utilities", value="Standard utilities")
        
        # Outdoor
        OutdoorSpaces.objects.create(home=home, title="Outdoor", value="Outdoor space available")
