# Architecture Notes

## Core Concepts

### Master Cards

A `card` is a master catalog record from a Pokemon card data source. It represents a known card in the broader universe, not something the user necessarily owns.

Examples of likely fields later:

- external card ID
- name
- set
- collector number
- rarity
- images
- types and attributes

This model should stay distinct from ownership and organization.

### Collection Entries

A `collectionEntry` is a user-owned record tied to a master card. This is the model that represents ownership.

Examples of decisions you still need to make:

- Does one row represent one physical copy?
- Or does one row represent a grouped quantity of copies with shared attributes?
- Which copy-specific fields belong here, such as condition, finish, purchase notes, or grading data?

Collection entries belong to users and may be assigned to binders.

### Binders

A `binder` is a user-created organizational group. It should organize `collectionEntry` records, not master `card` records.

That distinction matters because:

- the same master card can appear multiple times in a user collection
- different copies may have different condition or finish
- a user may want one copy in a display binder and another in a trade binder

## Why Scan Confirmation Is Required

Scan results should produce candidate matches, not automatic saves.

Reasons:

- OCR and visual recognition will sometimes be ambiguous
- different printings can look very similar
- the app may identify the right master card but still need user input for binder, quantity, condition, or finish
- accidental auto-save would pollute the collection and make later cleanup frustrating

Recommended flow:

1. user scans a card
2. system creates a `scanSession`
3. system returns ranked `scanCandidates`
4. user confirms the likely card
5. app opens an add-to-collection step before final save

## Why Manual Add Comes Before Scan

Manual add should be the first production milestone because it validates the core product model before recognition is introduced.

Benefits:

- proves the collection and binder model is sound
- lets you design schema decisions around real ownership flows
- keeps the frontend and backend useful even before OCR exists
- prevents scan work from blocking the basic app experience

If manual add is awkward, scan will only amplify that awkwardness.

## Suggested Schema Questions Before Migrations

### Cards

- What external source is authoritative for card identity?
- Will cards be fully mirrored locally or fetched on demand plus cached?
- Which fields are stable enough to store as canonical columns?

### Collection Entries

- Is quantity stored on the row, or is each physical copy its own row?
- How do condition, finish, language, grading, or notes vary across duplicates?
- Can one entry exist without a binder?

### Binders

- Are binders flat or nested?
- Can a binder be archived?
- Should binder ordering be user-controlled?

### Scan Sessions

- How long should scan history persist?
- Should raw uploads be stored, cropped images stored, or neither?
- What minimum audit trail do you want for candidate generation?

### Scan Candidates

- Do you store only top candidates, or full ranking output?
- Should confidence be normalized?
- What metadata explains why a match was suggested?

## Future Features To Keep In Mind

- authenticated multi-user ownership
- offline-friendly local caching
- card catalog sync jobs
- bulk import/export
- wishlist and trade tracking
- graded slab support
- scan history and review
- confidence tuning and feedback loops for candidate ranking
- image crop preview before OCR/ranking
- support for cards not yet present in the local catalog

