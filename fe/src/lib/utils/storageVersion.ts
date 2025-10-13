// Storage version management for local storage migrations
export const STORAGE_VERSION = '1.0.0'

export interface StorageVersionInfo {
  version: string
  migrated: boolean
}

export interface MigrationFunction {
  (data: any): any
}

export interface StorageMigrations {
  [version: string]: MigrationFunction
}

// Migration registry for document store
export const documentMigrations: StorageMigrations = {
  // Future migrations will be added here
  // Example:
  // '1.1.0': (data) => {
  //   // Migration logic for version 1.1.0
  //   return { ...data, newField: 'defaultValue' }
  // }
}

// Migration registry for theme store
export const themeMigrations: StorageMigrations = {
  // Future migrations will be added here
  // Example:
  // '1.1.0': (data) => {
  //   // Migration logic for version 1.1.0
  //   return { ...data, newThemeOption: true }
  // }
}

/**
 * Applies migrations to stored data based on version
 */
export function applyMigrations(
  storedData: any,
  migrations: StorageMigrations,
  currentVersion: string
): any {
  if (!storedData || !storedData.version) {
    // No version info, assume it's the current version
    return { ...storedData, version: currentVersion, migrated: false }
  }

  const storedVersion = storedData.version
  if (storedVersion === currentVersion) {
    return storedData
  }

  // Get all migration versions and sort them
  const migrationVersions = Object.keys(migrations).sort()
  
  // Find migrations to apply
  const migrationsToApply = migrationVersions.filter(version => 
    version > storedVersion && version <= currentVersion
  )

  let migratedData = { ...storedData }
  
  for (const version of migrationsToApply) {
    const migration = migrations[version]
    if (migration) {
      migratedData = migration(migratedData)
      migratedData.version = version
      migratedData.migrated = true
    }
  }

  // Set final version
  migratedData.version = currentVersion
  
  return migratedData
}

/**
 * Creates a versioned storage wrapper for Zustand persist
 */
export function createVersionedStorage(
  storageName: string,
  migrations: StorageMigrations
) {
  return {
    getItem: (name: string) => {
      let item = null;
      try {
        item = localStorage.getItem(name)
        if (!item) return null
        
        const parsed = JSON.parse(item)
        const migrated = applyMigrations(parsed, migrations, STORAGE_VERSION)
        
        return JSON.stringify(migrated)
      } catch (error) {
        console.warn(`Failed to migrate storage for ${storageName}:`, error)
        return item
      }
    },
    setItem: (name: string, value: any) => {
      try {
        const versioned = { ...value, version: STORAGE_VERSION }
        localStorage.setItem(name, JSON.stringify(versioned))
      } catch (error) {
        console.warn(`Failed to save versioned storage for ${storageName}:`, error)
        localStorage.setItem(name, JSON.stringify(value))
      }
    },
    removeItem: (name: string) => {
      localStorage.removeItem(name)
    }
  }
}
