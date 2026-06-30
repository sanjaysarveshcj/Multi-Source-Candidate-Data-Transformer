from app.projection.path_extractor import PathExtractor

class DynamicSchemaValidator:
    
    @staticmethod
    def validate(output: dict, config: dict):
        errors = []
        fields = config.get("fields", [])
        
        for field_cfg in fields:
            path = field_cfg.get("path")
            required = field_cfg.get("required", False)
            expected_type = field_cfg.get("type")
            
            if not path:
                continue
                
            val = PathExtractor.extract(output, path)
            
            is_missing = val is None or (isinstance(val, (list, dict, str)) and len(val) == 0)
            
            if required and is_missing:
                errors.append(f"Field '{path}' is required but missing or empty.")
                continue
                
            if not is_missing and expected_type:
                # Basic type checking
                if expected_type == "string" and not isinstance(val, str):
                    errors.append(f"Field '{path}' expected type string, got {type(val).__name__}.")
                elif expected_type == "string[]":
                    if not isinstance(val, list) or not all(isinstance(x, str) for x in val):
                        errors.append(f"Field '{path}' expected type string[].")
                elif expected_type == "number" and not isinstance(val, (int, float)):
                    errors.append(f"Field '{path}' expected type number, got {type(val).__name__}.")
                elif expected_type == "object" and not isinstance(val, dict):
                    errors.append(f"Field '{path}' expected type object, got {type(val).__name__}.")
                elif expected_type == "object[]":
                    if not isinstance(val, list) or not all(isinstance(x, dict) for x in val):
                        errors.append(f"Field '{path}' expected type object[].")
                        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
