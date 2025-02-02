ASM = ca65
LD = ld65
HEXDUMP = hexdump
SED = sed

SRC = $(wildcard *.s)

OBJ = $(SRC:.s=.o)

CFG = flat.cfg

BIN = $(SRC:.s=.bin)

all: $(BIN) dump

# Assemble all .s files into .o files
$(OBJ): %.o: %.s
	$(ASM) $< -o $@

# Link the object files into the final binary for each source file
%.bin: %.o
	$(LD) -o $@ -C $(CFG) $<

# Dump the raw binary
dump: $(BIN)
	@echo "Binaries:"
	@for bin in $(BIN); do \
		echo "$$bin"; \
		$(HEXDUMP) -v -e '1/1 "%02X,"' $$bin; \
		echo; \
	done

# Clean up object files and the binary
clean:
	rm -f $(OBJ) $(BIN)
