# Unified Plant ID (UPID) System

A comprehensive system for mapping plant/vegetable data across all global databases, languages, and regional naming conventions.

## Overview

The UPID system creates a single canonical identifier for every edible plant that links to:
- Scientific nomenclature (binomial names)
- Names in 100+ languages (including regional dialects)
- External databases (Wikidata, Trefle, USDA, OpenFarm, etc.)
- Toxicity data for pets/animals (ASPCA verified)
- Growing requirements
- Nutritional information
- Culinary usage patterns
- Storage and preservation methods

## Project Structure

```
upid-system/
├── schema/
│   └── upid-core.ts          # TypeScript interfaces for UPID data structure
├── services/
│   ├── api-integrations.ts   # External API connectors
│   └── search-service.ts     # Multi-language fuzzy search
├── data/
│   └── examples/
│       └── tomato-UPID-FRT-0001.json  # Example UPID entry
└── README.md
```

## Core Components

### 1. UPID Schema (`schema/upid-core.ts`)

Defines the complete data structure for a plant entry:

- **Taxonomy**: Scientific classification (kingdom → species)
- **External IDs**: Mappings to Wikidata, Trefle, USDA, OpenFarm, ASPCA, etc.
- **Names**: Multi-language support with:
  - Common names in 100+ languages
  - Regional variations (e.g., "Jitomate" in Mexico vs "Tomate" in Spain)
  - Romanized/transliterated versions
  - Phonetic representations (IPA)
- **Varieties**: Cultivar-specific data (Cherokee Purple, Roma, etc.)
- **Plant Parts**: Edibility and toxicity per part (fruit vs. leaves)
- **Toxicity**: Species-specific toxicity data for pets
- **Growing**: Complete growing requirements
- **Culinary**: Cuisine usage, dishes, substitutes
- **Nutrition**: USDA-sourced nutritional data
- **Storage**: Fresh storage and preservation methods

### 2. API Integrations (`services/api-integrations.ts`)

Connectors for external data sources:

| Service | Data Provided | Free Tier |
|---------|--------------|-----------|
| **Wikidata** | Multi-language names, taxonomy | Unlimited |
| **Trefle.io** | Growing requirements, edibility | 120 req/min |
| **USDA FoodData Central** | Nutrition data | 1000 req/hour |
| **OpenFarm** | Growing guides, companions | Unlimited |
| **ASPCA** | Pet toxicity data | Cached/scraped |
| **FAO AGROVOC** | Agricultural vocabulary (40+ languages) | Unlimited |
| **Spoonacular** | Recipe parsing, ingredients | 150 req/day |
| **Google Translate** | Translation, language detection | Paid |
| **Open-Meteo** | Weather, soil conditions | Unlimited |

### 3. Search Service (`services/search-service.ts`)

Multi-language fuzzy search capabilities:

- **Text Normalization**: Handles diacritics, whitespace, case
- **Script Detection**: Identifies Devanagari, Han, Arabic, Cyrillic, etc.
- **Fuzzy Matching**: Jaro-Winkler similarity for name matching
- **Transliteration**: Converts non-Latin scripts to searchable forms
- **Language Detection**: Automatic language identification
- **Recipe Matching**: Extracts vegetables from ingredient lists

## UPID Format

```
UPID-{CATEGORY}-{NUMBER}[-VAR-{VARIETY_NUMBER}]

Categories:
- VEG: Vegetables
- HRB: Culinary herbs  
- FRT: Fruits grown as vegetables (tomato, pepper)
- LEG: Legumes
- TBR: Tubers and roots
- ALM: Alliums
- MSH: Mushrooms
- SPR: Sprouts and microgreens

Examples:
- UPID-FRT-0001         → Tomato (base species)
- UPID-FRT-0001-VAR-001 → Cherokee Purple tomato
- UPID-ALM-0001         → Onion
- UPID-HRB-0001         → Basil
```

## Usage Example

```typescript
import { PlantSearchService, BulkPlantImporter } from './services/search-service';
import { UnifiedPlantDataBuilder } from './services/api-integrations';

// Initialize search service
const searchService = new PlantSearchService();

// Build UPID from scientific name (fetches from all APIs)
const builder = new UnifiedPlantDataBuilder();
const tomatoData = await builder.buildFromScientificName(
  'Solanum lycopersicum', 
  'UPID-FRT-0001'
);

// Import into search index
const importer = new BulkPlantImporter(searchService);
importer.importFromUPIDData([tomatoData]);

// Search in any language
const results = searchService.search('टमाटर');  // Hindi for tomato
// Returns: [{ upid: 'UPID-FRT-0001', matchedName: 'टमाटर', score: 1.0 }]

const results2 = searchService.search('pomodoro');  // Italian
// Returns: [{ upid: 'UPID-FRT-0001', matchedName: 'Pomodoro', score: 1.0 }]

const results3 = searchService.search('tamatar');  // Romanized Hindi
// Returns: [{ upid: 'UPID-FRT-0001', matchedName: 'Tamatar', score: 0.95 }]
```

## API Keys Required

```bash
# .env file
TREFLE_API_KEY=your_trefle_key
USDA_API_KEY=your_usda_key
GOOGLE_TRANSLATE_API_KEY=your_google_key
SPOONACULAR_API_KEY=your_spoonacular_key
```

## Language Coverage

The system supports names in:

| Language | Script | Coverage |
|----------|--------|----------|
| English | Latin | Primary |
| Spanish | Latin | Full |
| Hindi | Devanagari | Full |
| Chinese | Han | Full |
| Arabic | Arabic | Full |
| Japanese | Kanji/Kana | Full |
| Korean | Hangul | Full |
| Tamil | Tamil | Full |
| Telugu | Telugu | Full |
| Bengali | Bengali | Full |
| + 90 more... | Various | Wikidata-sourced |

## Pet Toxicity Coverage

ASPCA-verified toxicity data for:
- Dogs
- Cats
- Horses
- Rabbits
- Guinea pigs
- Birds
- Chickens

Each plant entry includes:
- Toxic parts (leaves, stems, fruit, etc.)
- Severity level (mild → fatal)
- Toxic compounds
- Symptoms
- Treatment notes

## Integration with Family Food Self-Sufficiency AI

This UPID system serves as the plant knowledge base for the larger self-sufficiency project:

1. **Consumption Calculator**: Uses UPID for vegetable identification in any language
2. **Recipe Decomposition**: Maps recipe ingredients to UPID entries
3. **Pet Safety**: Filters growing recommendations based on household pets
4. **Growing Planner**: Uses UPID growing data for planting schedules
5. **Multi-language Support**: Allows families to input in their native language

## Next Steps

1. **Seed the database**: Run bulk import from Trefle vegetable list
2. **Scrape ASPCA**: Build cached toxicity database
3. **Add more regional vegetables**: South Asian, East Asian, African varieties
4. **Build variety database**: Common cultivars for each species
5. **Create REST API**: Expose search as microservice

## License

MIT
